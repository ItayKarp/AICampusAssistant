import json
import os
from pathlib import Path

from pydantic import ValidationError

from domain.ai.schemas import ClassificationOutput
from dotenv import load_dotenv
from openai import OpenAI


load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

SYSTEM_INSTRUCTIONS_PATH = Path(__file__).resolve().parent / "classifier_system_instructions.txt"
SYSTEM_INSTRUCTION = SYSTEM_INSTRUCTIONS_PATH.read_text(encoding="utf-8")

class AIClassifierService:
    def __init__(self, model_name = "gpt-4o-mini",ai_client = client, system_instruction = SYSTEM_INSTRUCTION):
        self.client = ai_client
        self.model_name = model_name
        self.system_instruction = system_instruction

    def classify(self, question) -> ClassificationOutput:
        raw_response = self._generate_classification(question)
        parsed_response = self._parse_response(raw_response)
        return parsed_response

    def _generate_classification(self, question) -> str:
        try:
            response = self.client.responses.create(
                model=self.model_name,
                input=question,
                instructions=self.system_instruction,
                timeout=8.0
                )

            return response.output_text
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise

    @staticmethod
    def _parse_response(raw_response: str) -> ClassificationOutput:
        if not raw_response or not raw_response.strip():
            raise ValueError("Classifier returned an empty response.")

        cleaned = raw_response.strip()

        if cleaned.startswith("```json"):
            cleaned = cleaned[len("```json"):].strip()
        elif cleaned.startswith("```"):
            cleaned = cleaned[len("```"):].strip()

        if cleaned.endswith("```"):
            cleaned = cleaned[:-3].strip()

        try:
            data = json.loads(cleaned)
        except json.JSONDecodeError as error:
            raise ValueError(f"Classifier returned invalid JSON: {error}. Raw response: {repr(raw_response)}")

        try:
            return ClassificationOutput.model_validate(data)
        except ValidationError as error:
            raise ValueError(f"Classifier returned JSON with invalid schema: {error}. Parsed data: {data}")
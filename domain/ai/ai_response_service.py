import json
import os
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

SYSTEM_INSTRUCTIONS_PATH = Path(__file__).resolve().parent / "responder_system_instructions.txt"
RESPONSE_SYSTEM_INSTRUCTIONS = SYSTEM_INSTRUCTIONS_PATH.read_text(encoding="utf-8")


class AIResponseService:
    def __init__(
        self,
        model_name: str = "gpt-4o-mini",
        ai_client: OpenAI = client,
        system_instruction: str = RESPONSE_SYSTEM_INSTRUCTIONS,
    ):
        self.client = ai_client
        self.model_name = model_name
        self.system_instruction = system_instruction

    def generate_answer(self,question: str,table: str,rows: list[dict[str, Any]],) -> dict[str, Any]:
        payload = {
            "question": question,
            "table": table,
            "rows": rows,
        }

        response = self.client.responses.create(
            model=self.model_name,
            instructions=self.system_instruction,
            input=json.dumps(payload, ensure_ascii=False),
        )

        return json.loads(response.output_text)
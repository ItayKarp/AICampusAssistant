from pathlib import Path
import os

import json
from google import genai
from dotenv import load_dotenv
from google.genai.types import GenerateContentConfig

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_INSTRUCTIONS_PATH = Path(__file__).resolve().parent / "responder_system_instructions.txt"
SYSTEM_INSTRUCTION = SYSTEM_INSTRUCTIONS_PATH.read_text(encoding="utf-8")

def respond(user_question: str, classification_dict: dict, data: dict | list | None) -> str:
    payload = {
        "user_question": user_question,
        "classification": classification_dict,
        "database_result": data,
    }
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=json.dumps(payload, ensure_ascii=False, default=str),
            config=GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION,
                temperature=0.2,
            ),
        )
    except Exception as e:
        print(f"Error: {e}")
        raise RuntimeError("Failed to generate response. Please try again later.")
    return response.text
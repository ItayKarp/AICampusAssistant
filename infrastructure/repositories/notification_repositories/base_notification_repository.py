from contextlib import contextmanager
import json
from pathlib import Path
import os

from google import genai
from dotenv import load_dotenv
from google.genai.errors import ClientError
from google.genai.types import GenerateContentConfig

from infrastructure.db.database import Session
load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_INSTRUCTIONS_PATH = Path(__file__).resolve().parent / "ai_notification_system_instructions.txt"
SYSTEM_INSTRUCTION = SYSTEM_INSTRUCTIONS_PATH.read_text(encoding="utf-8")

class BaseNotificationRepository:
    def __init__(self, session_factory=Session):
        self.session_factory = session_factory

    @contextmanager
    def context_manager(self):
        session = self.session_factory()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def get_notification_details(payload):
        try:
            response = client.models.generate_content(
                model="gemini-2.5-flash-lite",
                contents=payload,
                config=GenerateContentConfig(
                    system_instruction=SYSTEM_INSTRUCTION
                )
            )
        except ClientError as e:
            print(f"Error: {e}")
            raise RuntimeError("Failed to generate response. Please try again later.")
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise
        try:
            return json.loads(response.text)
        except json.JSONDecodeError:
            print(f"Invalid JSON returned by model: {response.text}")
            raise RuntimeError("Failed to parse response. Please try again later.")
from contextlib import contextmanager
import json
from pathlib import Path
import os

from dotenv import load_dotenv
from openai import OpenAI

from infrastructure.db.database import Session
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=OPENAI_API_KEY)

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
            response = client.responses.create(
                model="gpt-4o-mini",
                instructions=SYSTEM_INSTRUCTION,
                input=payload
            )
        except Exception as e:
            print(f"Unexpected error: {e}")
            raise
        try:
            return json.loads(response.output_text)
        except json.JSONDecodeError:
            print(f"Invalid JSON returned by model: {response.text}")
            raise RuntimeError("Failed to parse response. Please try again later.")
from pathlib import Path
import os

from google import genai
from dotenv import load_dotenv
from google.genai.errors import ClientError
from google.genai.types import GenerateContentConfig

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_INSTRUCTIONS_PATH = Path(__file__).resolve().parent / "classifier_system_instructions.txt"
SYSTEM_INSTRUCTION = SYSTEM_INSTRUCTIONS_PATH.read_text(encoding="utf-8")

def classify_prompt(prompt: str):
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash-lite",
            contents=prompt,
            config=GenerateContentConfig(
                system_instruction=SYSTEM_INSTRUCTION
            )
        )
        return response.text
    except ClientError as e:
        print(f"Error: {e}")
        raise RuntimeError("AI quota exceeded. Please try again later.")
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise

if __name__ == "__main__":
    print(classify_prompt("When is my database systems exam?"))
import httpx
from dotenv import load_dotenv
import os

from fastapi import HTTPException

load_dotenv()

NEON_BASE_AUTH=os.getenv("NEON_BASE_AUTH")

class ResetPasswordRepository:
    def __init__(self):
        pass

    @staticmethod
    def reset_password(payload):
        with httpx.Client() as client:
            response = client.post(
                f"{NEON_BASE_AUTH}/auth/reset-password",
                json={
                    "token": payload.get("token"),
                    "password": payload.get("password")
                }
            )
        if not response.is_success:
            raise HTTPException(status_code=response.status_code, detail=response.json().get("message"))
        return response.json()

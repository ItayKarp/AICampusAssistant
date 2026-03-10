import httpx
from fastapi import HTTPException, Request
from dotenv import load_dotenv
import os
from .dtos import Register as Register_DTO

load_dotenv()

NEON_BASE_AUTH=os.getenv("NEON_BASE_AUTH")

class Register:
    def __init__(self):
        pass

    @staticmethod
    def register(payload: Register_DTO, request: Request):
        with httpx.Client() as client:
            response = client.post(
                f"{NEON_BASE_AUTH}/auth/sign-up/email",
                json={
                    "name": payload.name,
                    "email": payload.email,
                    "password": payload.password
                },
                headers={"Origin": str(request.base_url).rstrip("/")},
            )
        data = response.json()
        if not response.is_success:
            raise HTTPException(status_code=response.status_code, detail=data.get("message", "Signup failed"))
        return {"token": data["token"], "user": data["user"]}

import httpx
from fastapi import HTTPException, Request
from dotenv import load_dotenv
import os
from .dtos import Login as Login_DTO

load_dotenv()

NEON_BASE_AUTH=os.getenv("NEON_BASE_AUTH")

class Login:
    def __init__(self):
        pass

    @staticmethod
    def login_user(body: Login_DTO, request: Request):
        with httpx.Client() as client:
            response = client.post(
                f"{NEON_BASE_AUTH}/auth/sign-in/email",
                json={"email": body.email, "password": body.password},
                headers={"Origin": str(request.base_url).rstrip("/")}
            )
        data = response.json()
        if not response.is_success:
            raise HTTPException(status_code=response.status_code, detail=data.get("message"))
        return {"token": data["token"], "user": data["user"]}
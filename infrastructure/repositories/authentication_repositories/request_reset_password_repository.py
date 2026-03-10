import httpx
from fastapi import Request, HTTPException
from dotenv import load_dotenv
import os
load_dotenv()

NEON_BASE_AUTH=os.getenv("NEON_BASE_AUTH")


class RequestResetPasswordRepository:
    def __init__(self):
        pass

    @staticmethod
    def request_reset_password(email):
        with httpx.Client() as client:
            response = client.post(
                f"{NEON_BASE_AUTH}/auth/request-reset-password",
                json={
                    "email": email,
                    "redirectTo": f"www.itaykarpov.com/hackathon/reset-password"
                },
                headers={"Origin": "hackathon.itaykarpov.com/"}
            )
        if not response.is_success:
            raise HTTPException(status_code=response.status_code, detail=response.json().get("message"))
        return response.json()
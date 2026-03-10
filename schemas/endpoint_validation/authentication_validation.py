from pydantic import BaseModel, EmailStr

class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str


class LoginRequest(BaseModel):
    email: EmailStr
    password: str

class RequestPasswordReset(BaseModel):
    token: str
    email: EmailStr

class ResetPassword(BaseModel):
    token: str
    newPassword: str

class ForgotPassword(BaseModel):
    email: EmailStr
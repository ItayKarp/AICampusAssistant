from fastapi import APIRouter, Request, Header, HTTPException
from pygments.lexers import q

from services.authentication_handler_service import AuthenticationHandlerService
from infrastructure.repositories.authentication_repositories import Login, Register, RequestResetPasswordRepository, ResetPasswordRepository
from schemas.endpoint_validation.authentication_validation import LoginRequest, SignupRequest, ForgotPassword
from api.dependencies import get_user_id_and_email
from infrastructure.repositories.user_data_repositories.new_user_create_repository import CreateNewUser


authentication_router = APIRouter(prefix="/auth", tags=["authentication"])




@authentication_router.get("/")
def verify_jwt(authorization: str = Header(...)):
    # Expected header: Authorization: Bearer <token>
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")

    token = authorization.removeprefix("Bearer ").strip()
    use_case = AuthenticationHandlerService()
    return use_case.handle_verify_jwt(token)

@authentication_router.post("/login")
async def login(body: LoginRequest, request: Request):
    use_case = AuthenticationHandlerService(login_repository=Login)
    return use_case.handle_login(body, request)

@authentication_router.post("/register")
async def register(body: SignupRequest, request: Request):
    use_case =  AuthenticationHandlerService(register_repository=Register, new_user_repository=CreateNewUser)
    return use_case.handle_register(body, request)

@authentication_router.post("/reset-password")
async def reset_password(password: str, authorization: str = Header(...)):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = authorization.removeprefix("Bearer ").strip()
    use_case = AuthenticationHandlerService()
    token = use_case.handle_verify_jwt(token)
    payload = {"token": token, "password": password}
    if token:
        use_case = AuthenticationHandlerService(request_reset_password_repository=RequestResetPasswordRepository)
        return use_case.handle_reset_password(payload, password)
    else:
        raise HTTPException(status_code=401, detail="Invalid token")

@authentication_router.post("/request-reset-password")
async def request_reset_password(authorization: str = Header(...)):
    user_id, email = get_user_id_and_email(authorization)
    use_case = AuthenticationHandlerService(reset_password_repository=ResetPasswordRepository)
    return use_case.handle_request_reset_password(email)

@authentication_router.post("/forgot-password")
async def forgot_password(body: ForgotPassword):
    use_case = AuthenticationHandlerService(reset_password_repository=ResetPasswordRepository)
    return use_case.handle_request_reset_password(body.email)
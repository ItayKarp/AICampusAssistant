from fastapi import APIRouter, Header

from infrastructure.repositories.user_data_repositories import LoadUserDataRepository
from api.dependencies import get_user_id_and_email
from infrastructure.repositories.user_data_repositories.new_user_create_repository import CreateNewUser
from schemas.endpoint_validation.user_validation import Student
from services.load_personnel_handler_service import LoadPersonnelHandlerService
from services.user_handler_service import UserHandlerService

load_router = APIRouter(prefix="/load-personnel-data", tags=["load-personnel-data"])

@load_router.get("/load-personnel-data")
async def load_personnel_data(authorization: str = Header(...)):
    user_id, email = get_user_id_and_email(authorization)
    use_case = LoadPersonnelHandlerService(LoadUserDataRepository())
    return use_case.handle_load_personnel(email)

@load_router.post("/setup")
async def load_personnel_data_by_id(body: Student, authorization: str = Header(...)):
    user_id, email = get_user_id_and_email(authorization)
    use_case = UserHandlerService(new_account_setup_repository=CreateNewUser)
    return use_case.setup_new_user(email, body)
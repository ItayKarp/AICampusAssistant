from fastapi import APIRouter, Header

from infrastructure.repositories.user_data_repositories import LoadUserDataRepository
from api.dependencies import get_user_id_and_email
from infrastructure.repositories.user_data_repositories.new_account_setup_repository import NewAccountSetupRepository
from schemas.endpoint_validation.user_validation import Student
from services.user_handler_service import UserHandlerService

load_router = APIRouter(prefix="/load-personnel-data", tags=["load-personnel-data"])

@load_router.get("/")
async def load_personnel_data(authorization: str = Header(...)):
    user_id, email, supabase_user_id = get_user_id_and_email(authorization)
    use_case = UserHandlerService(LoadUserDataRepository())
    return use_case.handle_load_personnel(user_id)

@load_router.post("/setup")
async def load_personnel_data_by_id(body: Student, authorization: str = Header(...)):
    user_id, email, supabase_user_id = get_user_id_and_email(authorization)
    use_case = UserHandlerService(new_account_setup_repository=NewAccountSetupRepository())
    return use_case.setup_new_user(user_id, body)
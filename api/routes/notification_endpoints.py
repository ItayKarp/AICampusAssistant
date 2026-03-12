from fastapi import APIRouter, Header
from api.dependencies import get_user_id_and_email
from infrastructure.repositories.notification_repositories.notification_repository import CreateNotificationRepository
from services.notification_handler_service import NotificationHandlerService

notification_router = APIRouter(prefix="/notifications", tags=["notification"])


@notification_router.get("")
async def get_notifications(authorization: str = Header(...)):
    user_id, email, supabase_user_id = get_user_id_and_email(authorization)
    use_case = NotificationHandlerService(CreateNotificationRepository())
    return use_case.get_notifications(user_id)
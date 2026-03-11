from fastapi import APIRouter, Header

from api.dependencies import get_user_id_and_email
from infrastructure.repositories.announcements_repositories.create_announcement_repository import \
    CreateAnnouncementRepository
from infrastructure.repositories.announcements_repositories.get_announcements_repository import GetAnnouncements
from schemas.endpoint_validation.announcements_validation import CreateAnnouncementSchema
from services.announcements_handler_service import AnnouncementsHandlerService

management_router = APIRouter(prefix="/management", tags=["management"])

@management_router.get("/announcements")
async def announcements(authorization: str = Header(...)):
    user_id, email, supabase_user_id = get_user_id_and_email(authorization)
    use_case =  AnnouncementsHandlerService(GetAnnouncements())
    return use_case.handle_management_announcements(user_id)

@management_router.post("/announcements")
async def announcements(body: CreateAnnouncementSchema,authorization: str = Header(...)):
    user_id, email, supabase_user_id = get_user_id_and_email(authorization)
    use_case = AnnouncementsHandlerService(CreateAnnouncementRepository())
    return use_case.handle_create_announcements(body, user_id)
from fastapi import APIRouter, Header

from infrastructure.repositories.announcements_repositories.delete_announcements_repository import \
    DeleteAnnouncementsRepository
from infrastructure.repositories.announcements_repositories.get_announcements_repository import GetAnnouncements
from infrastructure.repositories.announcements_repositories.update_announcements_repository import \
    UpdateAnnouncementsRepository
from schemas.endpoint_validation.announcements_validation import CreateAnnouncementSchema
from services.announcements_handler_service import AnnouncementsHandlerService
from infrastructure.repositories.announcements_repositories.create_announcement_repository import CreateAnnouncementRepository
from api.dependencies import get_user_id_and_email

announcements_router = APIRouter(tags=["announcements"])

@announcements_router.post("/announcements")
async def announcements(body: CreateAnnouncementSchema,authorization: str = Header(...)):
    user_id, email = get_user_id_and_email(authorization)
    use_case = AnnouncementsHandlerService(CreateAnnouncementRepository())
    return use_case.handle_create_announcements(body, user_id)


@announcements_router.get("/announcements")
async def announcements(authorization: str = Header(...)):
    user_id, email = get_user_id_and_email(authorization)
    use_case =  AnnouncementsHandlerService(GetAnnouncements())
    return use_case.handle_get_announcements(user_id)


@announcements_router.put("/announcements/{announcement_id}")
async def announcements(announcement_id: int,details, payload: CreateAnnouncementSchema,authorization: str = Header(...)):
    user_id, email = get_user_id_and_email(authorization)
    use_case = AnnouncementsHandlerService(UpdateAnnouncementsRepository())
    return use_case.handle_update_announcements(announcement_id, payload,details, user_id)


@announcements_router.delete("/announcements/{announcement_id}")
async def announcements(announcement_id: int,body,authorization: str = Header(...)):
    user_id, email = get_user_id_and_email(authorization)
    use_case = AnnouncementsHandlerService(DeleteAnnouncementsRepository())
    return use_case.handle_delete_announcements(announcement_id,body.get("details"), user_id)

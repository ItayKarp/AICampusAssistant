from datetime import datetime

from infrastructure.db.models import Announcement, AuditLog
from infrastructure.repositories.announcements_repositories.base_announcement_repository import BaseAnnouncementRepository

class UpdateAnnouncementsRepository(BaseAnnouncementRepository):
    def update(self,announcement_id, payload, user_id, details):
        with self.context_manager() as session:
            user = self.get_user(user_id, session)
            if user.role != "admin" or user.role != "management":
                raise ValueError("Unauthorized access")
            announcement = session.get(Announcement, announcement_id)
            if not announcement:
                raise ValueError(f"Announcement with id {announcement_id} not found")
            announcement.title = payload.title
            announcement.content = payload.content
            announcement.target_role = payload.target_role
            announcement.updated_at = datetime.now()
            session.flush(announcement)
            audit = AuditLog(
                actor_user_id=user_id,
                action_type="UPDATE_ANNOUNCEMENT",
                target_type="announcements",
                target_id=announcement_id,
                details=details,
                created_at=datetime.now()
            )
            session.add(audit)
            session.flush(audit)
            return announcement


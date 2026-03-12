from datetime import datetime

from infrastructure.db.models import Announcement, AuditLog
from infrastructure.repositories.announcements_repositories.base_announcement_repository import BaseAnnouncementRepository

class DeleteAnnouncementsRepository(BaseAnnouncementRepository):
    def delete(self,announcement_id, user_id, details):
        with self.context_manager() as session:
            user = self.get_user(user_id, session)
            if user.role != "admin" or user.role != "management":
                raise ValueError("Unauthorized access")
            announcement = session.get(Announcement, announcement_id)
            if not announcement:
                raise ValueError(f"Announcement with id {announcement_id} not found")
            session.delete(announcement)
            audit = AuditLog(
                actor_user_id=user_id,
                action_type="DELETE_ANNOUNCEMENT",
                target_type="announcements",
                target_id=announcement_id,
                details=details,
                created_at=datetime.now()
            )
            session.add(audit)
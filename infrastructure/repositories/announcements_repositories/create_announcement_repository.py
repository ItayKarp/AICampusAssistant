from datetime import datetime

from infrastructure.repositories.announcements_repositories.base_announcement_repository import BaseAnnouncementRepository
from infrastructure.db.models import Announcement, AuditLog


class CreateAnnouncementRepository(BaseAnnouncementRepository):
    def create(self, payload, user_id):
        with self.context_manager() as session:
            user = self.get_user(user_id, session)
            if user.role != "admin" or user.role != "management":
                raise ValueError("Unauthorized access")
            announcement = Announcement(**payload)
            session.add(announcement)
            session.flush(announcement)
            audit = AuditLog(
                actor_user_id=user_id,
                action_type="CREATE_ANNOUNCEMENT",
                target_type="announcements",
                target_id=announcement.id,
                details=payload.get("content"),
                created_at=datetime.now()
            )
            session.add(audit)
            session.flush(audit)
            return announcement

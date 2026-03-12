from datetime import datetime

from infrastructure.repositories.announcements_repositories.base_announcement_repository import BaseAnnouncementRepository
from infrastructure.db.models import Announcement, AuditLog


class CreateAnnouncementRepository(BaseAnnouncementRepository):
    def create(self, payload, user_id):
        with self.context_manager() as session:
            user = self.get_user(user_id, session)
            if not user:
                raise ValueError("User not found")
            if user.role != "admin" and user.role != "management":
                raise ValueError("Unauthorized access")
            announcement = Announcement(title= payload.title, content=payload.content, is_active=True, created_at=datetime.now(), target_role=payload.target_role, created_by=user.id)
            session.add(announcement)

            audit = AuditLog(
                actor_user_id=user_id,
                action_type="CREATE_ANNOUNCEMENT",
                target_type="announcements",
                target_id=announcement.id,
                details=payload.content,
                created_at=datetime.now()
            )
            session.add(audit)
            session.flush()

            return announcement

from fastapi import HTTPException

from ....infrastructure.db.models import Announcement
from ....infrastructure.repositories.announcements_repositories.base_announcement_repository import BaseAnnouncementRepository

class GetAnnouncements(BaseAnnouncementRepository):
    def get_announcements(self, user_id: int) -> list[dict]:
        with self.context_manager() as session:
            user = self.get_user(user_id, session)

            base_query = session.query(Announcement).filter(Announcement.is_active == True)

            if user.role == "admin":
                announcements = base_query.all()

            elif user.role == "student":
                announcements = (
                    base_query
                    .filter(Announcement.target_role == "student")
                    .all()
                )

            elif user.role == "management":
                announcements = (
                    base_query
                    .filter(Announcement.target_role.in_(["management", "student"]))
                    .all()
                )

            else:
                raise HTTPException(status_code=403, detail="Access denied")

            return [
                {
                    "id": announcement.id,
                    "title": announcement.title,
                    "content": announcement.content,
                    "target_role": announcement.target_role,
                    "is_active": announcement.is_active,
                    "created_at": (
                        announcement.created_at.isoformat()
                        if announcement.created_at else None
                    ),
                    "updated_at": (
                        announcement.updated_at.isoformat()
                        if announcement.updated_at else None
                    ),
                }
                for announcement in announcements
            ]

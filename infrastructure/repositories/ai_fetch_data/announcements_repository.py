from infrastructure.repositories.ai_fetch_data.base_ai_repository import BaseAIRepository
from infrastructure.db.models import Announcement


class SqlAlchemyAnnouncementsRepo(BaseAIRepository):
    def get_results(self, user_id: int | None = None) -> dict:
        with self.context_manager() as session:
            query = (
                session.query(Announcement)
                .filter(Announcement.is_active.is_(True))
                .order_by(Announcement.created_at.desc())
            )

            rows = query.limit(self.DEFAULT_LIMIT).all()

            return {
                "table": "announcements",
                "rows": [self._serialize_announcement(row) for row in rows],
            }

    def _serialize_announcement(self, row: Announcement) -> dict:
        return {
            "id": self.serialize_value(getattr(row, "id", None)),
            "title": self.serialize_value(getattr(row, "title", None)),
            "content": self.serialize_value(getattr(row, "content", None)),
            "target_role": self.serialize_value(getattr(row, "target_role", None)),
            "is_active": self.serialize_value(getattr(row, "is_active", None)),
            "created_by": self.serialize_value(getattr(row, "created_by", None)),
            "created_at": self.serialize_value(getattr(row, "created_at", None)),
            "updated_at": self.serialize_value(getattr(row, "updated_at", None)),
        }
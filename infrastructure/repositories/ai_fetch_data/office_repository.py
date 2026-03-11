from infrastructure.repositories.ai_fetch_data.base_ai_repository import BaseAIRepository
from infrastructure.db.models import Office


class SqlAlchemyOfficesRepo(BaseAIRepository):
    def get_results(self, user_id) -> dict:
        with self.context_manager() as session:
            rows = session.query(Office).limit(self.DEFAULT_LIMIT).all()
            return {
                "table": "offices",
                "rows": [self._serialize_office(row) for row in rows],
            }

    def _serialize_office(self, row: Office) -> dict:
        return {
            "id": self.serialize_value(getattr(row, "id", None)),
            "office_name": self.serialize_value(getattr(row, "office_name", None)),
            "room_number": self.serialize_value(getattr(row, "room_number", None)),
            "phone": self.serialize_value(getattr(row, "phone", None)),
            "email": self.serialize_value(getattr(row, "email", None)),
            "building": self.serialize_value(getattr(row, "building", None)),
            "staff_name": self.serialize_value(getattr(row, "staff_name", None)),
        }
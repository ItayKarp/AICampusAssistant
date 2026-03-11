from infrastructure.repositories.ai_fetch_data.base_ai_repository import BaseAIRepository
from infrastructure.db.models import OfficeOpeningHour


class SqlAlchemyOfficeOpeningHoursRepo(BaseAIRepository):
    def get_results(self, user_id) -> dict:
        with self.context_manager() as session:
            rows = session.query(OfficeOpeningHour).all()
            return {
                "table": "office_opening_hours",
                "rows": [self._serialize_office_opening_hour(row) for row in rows],
            }

    def _serialize_office_opening_hour(self, row: OfficeOpeningHour) -> dict:
        return {
            "id": self.serialize_value(getattr(row, "id", None)),
            "office_id": self.serialize_value(getattr(row, "office_id", None)),
            "day_of_week": self.serialize_value(getattr(row, "day_of_week", None)),
            "open_time": self.serialize_value(getattr(row, "open_time", None)),
            "close_time": self.serialize_value(getattr(row, "close_time", None)),
        }
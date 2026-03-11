from __future__ import annotations

from sqlalchemy import func, or_

from infrastructure.db.models import Course
from infrastructure.repositories.ai_fetch_data.base_ai_repository import BaseAIRepository


class SqlAlchemyCoursesRepo(BaseAIRepository):
    DEFAULT_COLUMNS = [
        "class_code",
        "class_name",
        "lecturer",
        "semester",
    ]

    def get_results(self,user_id) -> dict:
        with self.context_manager() as session:
            rows = session.query(Course).limit(self.DEFAULT_LIMIT).all()
            return {
                "table": "courses",
                "rows": [self._serialize_course(row) for row in rows],
            }

    def _serialize_course(self, row: Course) -> dict:
        return {
            "id": self.serialize_value(getattr(row, "id", None)),
            "class_code": self.serialize_value(getattr(row, "class_code", None)),
            "class_name": self.serialize_value(getattr(row, "class_name", None)),
            "lecturer": self.serialize_value(getattr(row, "lecturer", None)),
            "semester": self.serialize_value(getattr(row, "semester", None)),
        }
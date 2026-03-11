from infrastructure.repositories.ai_fetch_data.base_ai_repository import BaseAIRepository
from infrastructure.db.models import Exam


class SqlAlchemyExamsRepo(BaseAIRepository):
    def get_results(self, user_id) -> dict:
        with self.context_manager() as session:
            rows = session.query(Exam).limit(self.DEFAULT_LIMIT).all()
            return {
                "table": "exams",
                "rows": [self._serialize_exam(row) for row in rows],
            }

    def _serialize_exam(self, row: Exam) -> dict:
        return {
            "id": self.serialize_value(getattr(row, "id", None)),
            "course_id": self.serialize_value(getattr(row, "course_id", None)),
            "exam_date": self.serialize_value(getattr(row, "exam_date", None)),
            "exam_time": self.serialize_value(getattr(row, "exam_time", None)),
            "room": self.serialize_value(getattr(row, "room", None)),
            "type": self.serialize_value(getattr(row, "type", None)),
        }
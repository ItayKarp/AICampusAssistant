from app.infrastracture.db.models import Exam
from app.infrastracture.repositories.base_repository import BaseRepo
from app.infrastracture.repositories.helpers import (
    RepositoryClassificationHelper as ClassificationHelper,
    RepositoryResponseBuilder as ResponseBuilder,
    RepositoryResultSerializer as ResultSerializer
)


class SqlAlchemyExamRepo(BaseRepo):
    def get_results(
        self,
        classification: dict,
        user_question: str | None = None,
        user_id: int | None = None,
    ) -> dict:
        relevant_columns = ClassificationHelper.get_relevant_columns(classification)
        filters = ClassificationHelper.get_filters(classification)

        if not relevant_columns:
            return ResponseBuilder.empty("No relevant columns were provided.")

        with self.get_session() as session:
            query = session.query(Exam)

            course_id = self._parse_int(filters.get("course_id"))
            if filters.get("course_id") is not None and course_id is None:
                return ResponseBuilder.empty("Invalid course id filter.")
            if course_id is not None:
                query = query.filter(Exam.course_id == course_id)

            room = self._normalize_string(filters.get("room"))
            if room is not None:
                exact_match = query.filter(Exam.room.ilike(room))
                if exact_match.first():
                    query = exact_match
                else:
                    query = query.filter(Exam.room.ilike(f"%{room}%"))

            rows = query.limit(25).all()
            results = ResultSerializer.serialize_model_rows(rows, relevant_columns)

            return ResponseBuilder.success(
                results,
                empty_message="No matching exam records found.",
            )

    @staticmethod
    def _normalize_string(value: object) -> str | None:
        if value is None:
            return None

        if not isinstance(value, str):
            value = str(value)

        cleaned = value.strip()
        return cleaned if cleaned else None

    @staticmethod
    def _parse_int(value: object) -> int | None:
        if value is None or isinstance(value, bool):
            return None

        if isinstance(value, int):
            return value

        if isinstance(value, str):
            cleaned = value.strip()
            if not cleaned:
                return None
            try:
                return int(cleaned)
            except ValueError:
                return None

        return None
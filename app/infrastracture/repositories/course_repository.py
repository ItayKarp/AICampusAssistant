from app.infrastracture.db.models import Course
from app.infrastracture.repositories.base_repository import BaseRepo
from app.infrastracture.repositories.helpers import RepositoryResultSerializer,RepositoryClassificationHelper,RepositoryResponseBuilder


class SqlAlchemyCoursesRepo(BaseRepo):
    def get_results(
        self,
        classification: dict,
        user_question: str | None = None,
        user_id: int | None = None,
    ) -> dict:
        relevant_columns = RepositoryClassificationHelper.get_relevant_columns(classification)
        filters = RepositoryClassificationHelper.get_filters(classification)

        if not relevant_columns:
            return RepositoryResponseBuilder.empty("No relevant columns were provided.")

        with self.get_session() as session:
            query = session.query(Course)

            course_name = self._normalize_string(filters.get("course_name"))
            if course_name is not None:
                exact_match = query.filter(Course.class_name.ilike(course_name))
                if exact_match.first():
                    query = exact_match
                else:
                    query = query.filter(Course.class_name.ilike(f"%{course_name}%"))

            course_code = self._parse_int(filters.get("course_code"))
            if filters.get("course_code") is not None and course_code is None:
                return RepositoryResponseBuilder.empty("Invalid course code filter.")
            if course_code is not None:
                query = query.filter(Course.class_code == course_code)

            rows = query.limit(25).all()
            results = RepositoryResultSerializer.serialize_model_rows(rows, relevant_columns)

            return RepositoryResponseBuilder.success(
                results,
                empty_message="No matching course records found.",
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
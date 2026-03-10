from sqlalchemy import or_

from infrastructure.db.models import Course
from infrastructure.repositories.ai_fetch_data.base_ai_repository import BaseAIRepository as BaseRepo
from infrastructure.repositories.ai_fetch_data.helpers import (
    RepositoryClassificationHelper as ClassificationHelper,
    RepositoryResponseBuilder as ResponseBuilder,
    RepositoryResultSerializer as ResultSerializer,
)


class SqlAlchemyCoursesRepo(BaseRepo):
    def get_results(
        self,
        classification: dict,
        user_question: str | None = None,
        user_id: int | None = None,
    ) -> dict:
        category = ClassificationHelper.get_category(classification)
        table = ClassificationHelper.get_table(classification)
        relevant_columns = ClassificationHelper.get_relevant_columns(classification)
        filters = ClassificationHelper.get_filters(classification)

        if not relevant_columns:
            return ResponseBuilder.error(
                category=category,
                table=table,
                applied_filters=filters,
                message="No relevant columns were provided.",
            )

        with self.context_manager() as session:
            query = session.query(Course)

            class_name = ClassificationHelper.normalize_string(filters.get("class_name"))
            course_code = ClassificationHelper.normalize_string(filters.get("course_code"))
            semester = ClassificationHelper.normalize_string(filters.get("semester"))

            if class_name:
                query = query.filter(
                    or_(
                        Course.class_name.ilike(f"%{class_name}%"),
                        Course.class_name.ilike(f"%{class_name}%"),
                    )
                )

            if course_code:
                query = query.filter(Course.class_code.ilike(f"%{course_code}%"))

            if semester:
                query = query.filter(Course.semester.ilike(f"%{semester}%"))

            results = query.all()

            if not results:
                return ResponseBuilder.empty(
                    category=category,
                    table=table,
                    applied_filters=filters,
                    message="No matching courses were found.",
                )

            serialized_results = ResultSerializer.serialize_rows(
                rows=results,
                relevant_columns=relevant_columns,
            )

            return ResponseBuilder.success(
                category=category,
                table=table,
                applied_filters=filters,
                results=serialized_results,
                message="Results found.",
            )
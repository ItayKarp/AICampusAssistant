from ....infrastructure.db.models import OfficeOpeningHour as OfficeHours, Office
from ....infrastructure.repositories.ai_fetch_data.base_ai_repository import BaseAIRepository as BaseRepo
from ....infrastructure.repositories.ai_fetch_data.helpers import (
    RepositoryClassificationHelper as ClassificationHelper,
    RepositoryResponseBuilder as ResponseBuilder,
)


class SqlAlchemyOfficeHoursRepo(BaseRepo):
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
            query = session.query(OfficeHours, Office).join(
                Office,
                OfficeHours.office_id == Office.id,
            )

            office_name = ClassificationHelper.normalize_string(filters.get("office_name"))
            day_of_week = ClassificationHelper.normalize_string(filters.get("day_of_week"))
            building = ClassificationHelper.normalize_string(filters.get("building"))
            room_number = ClassificationHelper.normalize_string(filters.get("room_number"))

            if office_name:
                query = query.filter(Office.office_name.ilike(f"%{office_name}%"))

            if day_of_week:
                query = query.filter(OfficeHours.day_of_week.ilike(f"%{day_of_week}%"))

            if building:
                query = query.filter(Office.building.ilike(f"%{building}%"))

            if room_number:
                query = query.filter(Office.room_number.ilike(f"%{room_number}%"))

            results = query.all()

            if not results:
                return ResponseBuilder.empty(
                    category=category,
                    table=table,
                    applied_filters=filters,
                    message="No matching office hours were found.",
                )

            serialized_results = []
            for office_hours, office in results:
                row = {}

                for column_name in relevant_columns:
                    if hasattr(office_hours, column_name):
                        row[column_name] = getattr(office_hours, column_name, None)
                    elif hasattr(office, column_name):
                        row[column_name] = getattr(office, column_name, None)
                    else:
                        row[column_name] = None

                serialized_results.append(row)

            return ResponseBuilder.success(
                category=category,
                table=table,
                applied_filters=filters,
                results=serialized_results,
                message="Results found.",
            )
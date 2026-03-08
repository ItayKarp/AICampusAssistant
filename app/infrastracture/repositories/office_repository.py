from app.infrastracture.db.models import Office, OfficeOpeningHour
from app.infrastracture.repositories.base_repository import BaseRepo
from app.infrastracture.repositories.helpers import (
    RepositoryClassificationHelper as ClassificationHelper,
    RepositoryResponseBuilder as ResponseBuilder,
    RepositoryResultSerializer as ResultSerializer
)


class SqlAlchemyOfficeRepo(BaseRepo):
    DAY_ALIASES = {
        "sun": "Sunday",
        "sunday": "Sunday",
        "mon": "Monday",
        "monday": "Monday",
        "tue": "Tuesday",
        "tues": "Tuesday",
        "tuesday": "Tuesday",
        "wed": "Wednesday",
        "wednesday": "Wednesday",
        "thu": "Thursday",
        "thur": "Thursday",
        "thurs": "Thursday",
        "thursday": "Thursday",
        "fri": "Friday",
        "friday": "Friday",
        "sat": "Saturday",
        "saturday": "Saturday",
    }

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
            query = (
                session.query(OfficeOpeningHour, Office)
                .join(Office, Office.id == OfficeOpeningHour.office_id)
            )

            office_name = self._normalize_string(filters.get("office_name"))
            if office_name is not None:
                exact_match = query.filter(Office.office_name.ilike(office_name))
                if exact_match.first():
                    query = exact_match
                else:
                    query = query.filter(Office.office_name.ilike(f"%{office_name}%"))

            day = self._normalize_day(filters.get("day"))
            if filters.get("day") is not None and day is None:
                return ResponseBuilder.empty("Invalid day filter.")
            if day is not None:
                query = query.filter(OfficeOpeningHour.day_of_week == day)

            rows = query.limit(50).all()
            results = ResultSerializer.serialize_joined_rows(rows, relevant_columns)

            return ResponseBuilder.success(
                results,
                empty_message="No matching office opening hour records found.",
            )

    @classmethod
    def _normalize_day(cls, value: object) -> str | None:
        normalized = cls._normalize_string(value)
        if normalized is None:
            return None

        return cls.DAY_ALIASES.get(normalized.lower())

    @staticmethod
    def _normalize_string(value: object) -> str | None:
        if value is None:
            return None

        if not isinstance(value, str):
            value = str(value)

        cleaned = value.strip()
        return cleaned if cleaned else None
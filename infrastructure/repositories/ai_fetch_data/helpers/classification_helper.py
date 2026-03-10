from typing import Any


class RepositoryClassificationHelper:
    @staticmethod
    def get_category(classification: dict[str, Any]) -> str:
        return str(classification.get("category", "")).strip()

    @staticmethod
    def get_table(classification: dict[str, Any]) -> str:
        return str(classification.get("table", "")).strip()

    @staticmethod
    def get_filters(classification: dict[str, Any]) -> dict[str, Any]:
        filters = classification.get("filters", {})
        return filters if isinstance(filters, dict) else {}

    @staticmethod
    def get_relevant_columns(classification: dict[str, Any]) -> list[str]:
        relevant_columns = classification.get("relevant_columns", [])
        if not isinstance(relevant_columns, list):
            return []

        return [
            str(column).strip()
            for column in relevant_columns
            if str(column).strip()
        ]

    @staticmethod
    def get_related_tables(classification: dict[str, Any]) -> list[str]:
        related_tables = classification.get("related_tables", [])
        if not isinstance(related_tables, list):
            return []

        return [
            str(table).strip()
            for table in related_tables
            if str(table).strip()
        ]

    @staticmethod
    def get_scope(classification: dict[str, Any]) -> str:
        return str(classification.get("scope", "unknown")).strip().lower()

    @staticmethod
    def get_intent(classification: dict[str, Any]) -> str:
        return str(classification.get("intent", "unknown")).strip().lower()

    @staticmethod
    def requires_user_context(classification: dict[str, Any]) -> bool:
        return bool(classification.get("requires_user_context", False))

    @staticmethod
    def get_confidence(classification: dict[str, Any]) -> float:
        confidence = classification.get("confidence", 0.0)

        try:
            return float(confidence)
        except (TypeError, ValueError):
            return 0.0

    @staticmethod
    def normalize_string(value: Any) -> str | None:
        if value is None:
            return None

        normalized = str(value).strip()
        return normalized if normalized else None

    @staticmethod
    def normalize_list(value: Any) -> list[str]:
        if not isinstance(value, list):
            return []

        cleaned: list[str] = []
        for item in value:
            normalized = RepositoryClassificationHelper.normalize_string(item)
            if normalized is not None:
                cleaned.append(normalized)

        return cleaned
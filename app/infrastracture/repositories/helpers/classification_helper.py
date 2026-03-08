class RepositoryClassificationHelper:
    @staticmethod
    def get_filters(classification: dict | None) -> dict:
        if not isinstance(classification, dict):
            return {}

        filters = classification.get("filters", {})
        return filters if isinstance(filters, dict) else {}

    @staticmethod
    def get_relevant_columns(classification: dict | None) -> list[str]:
        if not isinstance(classification, dict):
            return []

        relevant_columns = classification.get("relevant_columns", [])
        if not isinstance(relevant_columns, list):
            return []

        cleaned_columns = []
        for column in relevant_columns:
            if isinstance(column, str):
                column = column.strip()
                if column:
                    cleaned_columns.append(column)

        return list(dict.fromkeys(cleaned_columns))
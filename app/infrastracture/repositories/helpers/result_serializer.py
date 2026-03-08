from typing import Iterable, Any


class RepositoryResultSerializer:
    @staticmethod
    def serialize_model_rows(rows: Iterable[Any], relevant_columns: list[str]) -> list[dict]:
        results = []

        for row in rows:
            row_data = {}
            for column in relevant_columns:
                if hasattr(row, column):
                    value = getattr(row, column)
                    row_data[column] = str(value) if value is not None else None

            if row_data:
                results.append(row_data)

        return results

    @staticmethod
    def serialize_joined_rows(rows: Iterable[tuple], relevant_columns: list[str]) -> list[dict]:
        results = []
        seen = set()

        for row in rows:
            row_data = {}

            for entity in row:
                for column in relevant_columns:
                    if hasattr(entity, column):
                        value = getattr(entity, column)
                        row_data[column] = str(value) if value is not None else None

            if not row_data:
                continue

            row_key = tuple(sorted(row_data.items()))
            if row_key in seen:
                continue

            seen.add(row_key)
            results.append(row_data)

        return results
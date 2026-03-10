from typing import Any


class RepositoryResultSerializer:
    @staticmethod
    def serialize_row(row: Any,relevant_columns: list[str] | None = None ) -> dict[str, Any]:
        if row is None:
            return {}

        if relevant_columns:
            serialized: dict[str, Any] = {}
            for column_name in relevant_columns:
                serialized[column_name] = getattr(row, column_name, None)
            return serialized

        if hasattr(row, "__table__") and hasattr(row.__table__, "columns"):
            return {
                column.name: getattr(row, column.name, None)
                for column in row.__table__.columns
            }

        return {}

    @staticmethod
    def serialize_rows(rows: list[Any],relevant_columns: list[str] | None = None,) -> list[dict[str, Any]]:
        return [
            RepositoryResultSerializer.serialize_row(
                row=row,
                relevant_columns=relevant_columns,
            )
            for row in rows
        ]
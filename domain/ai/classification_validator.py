from typing import Any

from ...domain.ai.schemas import ClassificationOutput, ValidatedClassification
from ...domain.ai.rules import (
    CATEGORY_TABLE_MAP,
    CATEGORY_ALLOWED_COLUMNS,
    CATEGORY_ALLOWED_RELATED_COLUMNS,
    CATEGORY_ALLOWED_FILTERS,

)


class ClassificationValidator:
    def validate(self, classification: ClassificationOutput) -> ValidatedClassification:
        errors: list[str] = []

        category = classification.category.value
        table = classification.table
        relevant_columns = list(classification.relevant_columns)
        related_tables = list(classification.related_tables)
        filters = dict(classification.filters)
        requires_user_context = classification.requires_user_context
        has_permission = classification.has_permission
        scope = classification.scope
        intent = classification.intent
        confidence = classification.confidence

        table, table_errors = self._validate_table(category, table)
        errors.extend(table_errors)

        relevant_columns, column_errors = self._validate_columns(category, relevant_columns)
        errors.extend(column_errors)

        related_tables, related_table_errors = self._validate_related_tables(category, related_tables)
        errors.extend(related_table_errors)

        filters, filter_errors = self._validate_filters(category, filters)
        errors.extend(filter_errors)

        requires_user_context, scope_errors = self._validate_scope(
            requires_user_context=requires_user_context,
            scope=scope,
        )
        errors.extend(scope_errors)

        is_valid = len(errors) == 0

        return ValidatedClassification(
            category=classification.category,
            table=table,
            relevant_columns=relevant_columns,
            related_tables=related_tables,
            filters=filters,
            requires_user_context=requires_user_context,
            has_permission=has_permission,
            scope=scope,
            intent=intent,
            confidence=confidence,
            is_valid=is_valid,
            validation_errors=errors,
        )

    @staticmethod
    def _validate_table(category: str, table) -> tuple[Any, list[str]]:
        errors = []
        expected_table = CATEGORY_TABLE_MAP.get(category)

        if expected_table is None:
            errors.append(f"Unsupported category '{category}'.")
            return table, errors

        if table.value != expected_table:
            errors.append(
                f"Table '{table.value}' does not match category '{category}'. Expected '{expected_table}'."
            )

        return table, errors

    @staticmethod
    def _validate_columns(category: str, relevant_columns: list[str]) -> tuple[list[str], list[str]]:
        errors = []
        allowed_direct = CATEGORY_ALLOWED_COLUMNS.get(category, set())
        allowed_related = CATEGORY_ALLOWED_RELATED_COLUMNS.get(category, set())
        allowed_all = allowed_direct | allowed_related

        valid_columns = []
        for column in relevant_columns:
            if column in allowed_all:
                valid_columns.append(column)
            else:
                errors.append(f"Column '{column}' is not allowed for category '{category}'.")

        if not valid_columns:
            raise ValueError("No valid columns found.")

        return valid_columns, errors

    @staticmethod
    def _validate_related_tables(category: str, related_tables: list[str]) -> tuple[list[str], list[str]]:
        errors = []

        allowed_related_tables_map = {
            "exams": {"courses"},
            "office_opening_hours": {"offices"},
            "courses": set(),
            "faq": set(),
        }

        allowed_related_tables = allowed_related_tables_map.get(category, set())

        valid_related_tables = []
        for table in related_tables:
            if table in allowed_related_tables:
                valid_related_tables.append(table)
            else:
                errors.append(f"Related table '{table}' is not allowed for category '{category}'.")

        return valid_related_tables, errors

    @staticmethod
    def _validate_filters(category: str, filters: dict[str, Any]) -> tuple[dict[str, Any], list[str]]:
        errors = []
        allowed_filters = CATEGORY_ALLOWED_FILTERS.get(category, set())

        valid_filters = {}
        for key, value in filters.items():
            if key in allowed_filters:
                valid_filters[key] = value
            else:
                errors.append(f"Filter '{key}' is not allowed for category '{category}'.")

        return valid_filters, errors

    @staticmethod
    def _validate_scope(requires_user_context: bool, scope) -> tuple[bool, list[str]]:
        errors = []

        if scope.value == "self" and not requires_user_context:
            requires_user_context = True
            errors.append("Scope is 'self', so requires_user_context was forced to True.")

        return requires_user_context, errors
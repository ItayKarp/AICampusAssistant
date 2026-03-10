from typing import Any

from pydantic import BaseModel, Field
from ...domain.ai.enums import CategoryEnum, ScopeEnum, IntentEnum, TableEnum


class ClassificationOutput(BaseModel):
    category: CategoryEnum
    table: TableEnum
    relevant_columns: list[str] = Field(default_factory=list)
    related_tables: list[str] = Field(default_factory=list)
    filters: dict[str, Any] = Field(default_factory=dict)
    requires_user_context: bool = False
    has_permission: bool = False
    scope: ScopeEnum = ScopeEnum.UNKNOWN
    intent: IntentEnum = IntentEnum.UNKNOWN
    confidence: float = Field(default=0.0,ge=0.0,le=1.0)

class ValidatedClassification(BaseModel):
    category: CategoryEnum
    table: TableEnum
    relevant_columns: list[str] = Field(default_factory=list)
    related_tables: list[str] = Field(default_factory=list)
    filters: dict[str, Any] = Field(default_factory=dict)
    requires_user_context: bool = False
    has_permission: bool = False
    scope: ScopeEnum = ScopeEnum.UNKNOWN
    intent: IntentEnum = IntentEnum.UNKNOWN
    confidence: float = Field(default=0.0, ge=0.0, le=1.0)
    is_valid: bool = False
    validation_errors: list[str] = Field(default_factory=list)
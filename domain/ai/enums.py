from enum import Enum


class CategoryEnum(str, Enum):
    EXAMS = "exams"
    COURSES = "courses"
    FAQ = "faq"
    OFFICE_OPENING_HOURS = "office_opening_hours"


class ScopeEnum(str, Enum):
    SELF = "self"
    GLOBAL = "global"
    UNKNOWN = "unknown"


class IntentEnum(str, Enum):
    LOOKUP = "lookup"
    SEARCH = "search"
    LIST = "list"
    UNKNOWN = "unknown"


class TableEnum(str, Enum):
    EXAMS = "exams"
    COURSES = "courses"
    FAQ = "faq_items"
    OFFICE_OPENING_HOURS = "office_opening_hours"

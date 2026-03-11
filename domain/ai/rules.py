CATEGORY_TABLE_MAP = {
    "exams": "exams",
    "courses": "courses",
    "faq": "faq_items",
    "office_opening_hours": "office_opening_hours",
}

CATEGORY_ALLOWED_COLUMNS = {
    "exams": {"exam_date", "exam_time", "room", "type"},
    "courses": {"class_name", "lecturer", "class_code", "semester"},
    "faq": {"title", "question", "answer", "category"},
    "office_opening_hours": {"day_of_week", "open_time", "close_time"},
}

CATEGORY_ALLOWED_RELATED_COLUMNS = {
    "exams": {"class_name", "class_code", "lecturer", "semester"},
    "office_opening_hours": {"office_name", "building", "room_number", "phone", "email"},
    "courses": set(),
    "faq": set(),
}

CATEGORY_ALLOWED_FILTERS = {
    "exams": {"class_name", "class_code", "course_code", "lecturer", "semester", "room", "type", "date_from", "date_to", "exam_date"},
    "courses": {"class_name", "class_code", "course_code", "lecturer", "semester"},
    "faq": {"category", "title", "question", "search_text"},
    "office_opening_hours": {"office_name", "day_of_week", "open_time", "close_time", "building", "room_number"},
}

CATEGORY_DEFAULT_COLUMNS = {
    "exams": ["class_name", "class_code", "exam_date", "exam_time", "room", "type"],
    "courses": ["class_code", "class_name", "lecturer", "semester"],
    "faq": ["title", "question", "answer", "category"],
    "office_opening_hours": [
        "office_name",
        "building",
        "room_number",
        "day_of_week",
        "open_time",
        "close_time",
        "phone",
        "email",
    ],
}

CATEGORY_ALLOWED_RELATED_TABLES = {
    "exams": {"courses"},
    "office_opening_hours": {"offices"},
    "courses": set(),
    "faq": set(),
}
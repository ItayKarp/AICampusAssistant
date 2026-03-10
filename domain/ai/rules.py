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
    "exams": {"class_name"},
    "office_opening_hours": {"office_name"},
}

CATEGORY_ALLOWED_FILTERS = {
    "exams": {"class_name", "exam_date", "type"},
    "courses": {"class_name", "lecturer", "class_code", "semester"},
    "faq": {"category", "title", "question"},
    "office_opening_hours": {"office_name","day_of_week", "open_time", "close_time"},
}
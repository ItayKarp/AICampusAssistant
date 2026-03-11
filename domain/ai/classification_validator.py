ALLOWED_TABLES = {
    "courses",
    "exams",
    "offices",
    "office_opening_hours",
    "announcements",
}


class ClassificationValidator:
    def validate(self, classification):
        table = classification.table if hasattr(classification, "table") else classification.get("table")

        class Result:
            def __init__(self, table, is_valid):
                self.table = table
                self.is_valid = is_valid

            def model_dump(self):
                return {
                    "table": self.table,
                    "is_valid": self.is_valid,
                }

        return Result(table, table in ALLOWED_TABLES)
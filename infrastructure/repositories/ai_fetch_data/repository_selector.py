class RepositorySelector:
    def __init__(self, courses_repo, exams_repo, offices_repo, office_opening_hours_repo, announcements_repo):
        self.repos = {
            "courses": courses_repo,
            "exams": exams_repo,
            "offices": offices_repo,
            "office_opening_hours": office_opening_hours_repo,
            "announcements": announcements_repo,
        }

    def get_repository(self, table: str):
        return self.repos[table]
from datetime import datetime

from infrastructure.db.models import User, Student
from infrastructure.repositories.user_data_repositories.base_user_repository import BaseUserRepository


class LoadUserDataRepository(BaseUserRepository):
    def get_user_data(self, user_id):
        with self.context_manager() as session:
            student = session.query(Student).filter(Student.user_id == user_id).first()
            if not student:
                raise ValueError("Student not found")
            return {
                "first_name": student.first_name,
                "last_name": student.last_name,
                "major": student.major,
                "year": student.year,
            }
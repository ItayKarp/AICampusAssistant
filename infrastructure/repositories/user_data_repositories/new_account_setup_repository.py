from datetime import datetime
from fastapi import HTTPException

from infrastructure.db.models import User, Student
from infrastructure.repositories.user_data_repositories.base_user_repository import BaseUserRepository


class NewAccountSetupRepository(BaseUserRepository):
    def setup(self,user_id, body):
        with self.context_manager() as session:
            user = session.query(User).filter(User.id == user_id).first()
            if not user:
                raise HTTPException(status_code=409, detail="User does not exist.")
            student = session.query(Student).filter(Student.user_id == user_id).first()
            if student:
                raise HTTPException(status_code=409, detail="Student already exists.")
            student = Student(
                first_name=body.first_name,
                last_name=body.last_name,
                email=user.email,
                major=body.major,
                year=body.year,
                created_at=datetime.now(),
                user_id=user.id
            )
            session.add(student)
            return {"message": "Account created successfully"}
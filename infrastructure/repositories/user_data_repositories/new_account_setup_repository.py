from datetime import datetime
from fastapi import HTTPException

from infrastructure.db import User, Student
from infrastructure.repositories.user_data_repositories.base_user_repository import BaseUserRepository


class NewAccountSetupRepository(BaseUserRepository):
    def setup(self,email, body):
        with self.context_manager() as session:
            user = session.query(User).filter(User.email == email).first()
            if user:
                raise HTTPException(status_code=409, detail="User with this email already exists")
            student = Student(
                first_name=body.first_name,
                last_name=body.last_name,
                email=email,
                major=body.major,
                year=body.year,
                created_at=datetime.now(),

            )
            session.add(student)
            session.flush(student)
            return {"message": "Account created successfully", "account_id": user.id}
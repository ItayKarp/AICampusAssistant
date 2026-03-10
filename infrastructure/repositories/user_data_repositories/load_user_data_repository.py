from datetime import datetime

from ....infrastructure.db.models import User
from ....infrastructure.repositories.user_data_repositories.base_user_repository import BaseUserRepository


class LoadUserDataRepository(BaseUserRepository):
    def get_user_data(self, email):
        with self.context_manager() as session:
            user = session.query(User).filter(User.email == email).first()
            if not user:
                raise ValueError(
                    "User not found"
                )
            user.last_login = datetime.now()
            session.flush(user)
            return {
                "user_id": user.id,
                "user_name": user.name,
                "user_email": user.email,
                "user_role": user.role,
            }
from contextlib import contextmanager

from infrastructure.db.database import Session
from infrastructure.db.models import User


class BaseAnnouncementRepository:
    def __init__(self, session_factory=Session):
        self.session_factory = session_factory

    @contextmanager
    def context_manager(self):
        session = self.session_factory()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    @staticmethod
    def get_user(user_id: int, session):
        user = session.get(User, user_id)
        if not user:
            raise ValueError("User not found")
        return user

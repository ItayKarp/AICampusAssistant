from contextlib import contextmanager
from datetime import datetime

from infrastructure.db.models import User
from infrastructure.db.database import Session


class CreateNewUser:
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


    def create(self, email, password, name):
        with self.context_manager() as session:
            user = User(email=email, password_hash=password, name=name, created_at=datetime.now(), last_login_at=datetime.now(), role="student")
            session.add(user)
            session.flush(user)
            return user.id

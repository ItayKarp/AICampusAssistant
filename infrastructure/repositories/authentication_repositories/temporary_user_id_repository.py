from contextlib import contextmanager

from ....infrastructure.db.database import Session
from ....infrastructure.db.models import User


class TemporaryUserIdRepository:
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

    def add_temporary_user_id(self, user_id: int, email):
        with self.context_manager() as session:
            user = session.query(User).filter(User.email == email).first()
            user.neon_user_id = user_id
            session.flush(user)
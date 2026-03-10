from contextlib import contextmanager
from ....infrastructure.db.database import Session

class BaseUserRepository:
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

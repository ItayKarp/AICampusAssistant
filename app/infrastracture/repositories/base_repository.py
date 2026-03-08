from abc import abstractmethod, ABC
from contextlib import contextmanager
from sqlalchemy.exc import SQLAlchemyError

from app.infrastracture.db.database import Session


class BaseRepo(ABC):
    def __init__(self, session_factory=Session):
        self.session_factory = session_factory

    @contextmanager
    def get_session(self):
        session = self.session_factory()
        try:
            yield session
        except SQLAlchemyError:
            session.rollback()
            raise
        finally:
            session.close()

    @abstractmethod
    def get_results(self, classification:dict, user_question:str, user_id:int):
        pass

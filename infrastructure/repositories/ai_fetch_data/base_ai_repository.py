from abc import ABC, abstractmethod
from contextlib import contextmanager
from typing import Any

from ....infrastructure.db.database import Session


class BaseAIRepository(ABC):
    @abstractmethod
    def get_results(self,classification: dict[str, Any],user_question: str | None = None,user_id: int | None = None,) -> dict[str, Any]:
        raise NotImplementedError

    @contextmanager
    def context_manager(self):
        session = Session()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
from __future__ import annotations

from abc import ABC, abstractmethod
from contextlib import contextmanager
from datetime import date, datetime, time
from decimal import Decimal
from typing import Any
from uuid import UUID

from infrastructure.db.database import Session


class BaseAIRepository(ABC):
    DEFAULT_LIMIT = 50

    @contextmanager
    def context_manager(self):
        session = Session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @staticmethod
    def serialize_value(value: Any) -> Any:
        if isinstance(value, datetime):
            return value.isoformat()
        if isinstance(value, date):
            return value.isoformat()
        if isinstance(value, time):
            return value.strftime("%H:%M:%S")
        if isinstance(value, Decimal):
            return float(value)
        if isinstance(value, UUID):
            return str(value)
        return value
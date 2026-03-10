from contextlib import contextmanager

from fastapi import HTTPException
from ..infrastructure.db.database import Session
from ..infrastructure.db.models import User
from ..services.authentication_handler_service import AuthenticationHandlerService

@contextmanager
def context_manager(session_factory = Session):
    session = session_factory()
    try:
        yield session
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()



def get_user_id_and_email(authorization: str):
    if not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid authorization header")
    token = authorization.removeprefix("Bearer ").strip()
    use_case = AuthenticationHandlerService()
    payload = use_case.handle_verify_jwt(token)
    try:
        email = payload.get("email")
        with context_manager() as session:
            user = session.query(User).filter(User.email == email).first()
            if not user:
                raise ValueError("User not found")
        return user.id, user.email
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token")

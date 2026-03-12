from contextlib import contextmanager
import os

import jwt
from fastapi import Header, HTTPException
from jwt import PyJWKClient
from jwt.exceptions import InvalidTokenError

from infrastructure.db.database import Session
from infrastructure.db.models import User

SUPABASE_URL = os.getenv("SUPABASE_URL")
if not SUPABASE_URL:
    raise RuntimeError("SUPABASE_URL is not configured")
SUPABASE_JWKS_URL = f"{SUPABASE_URL.rstrip('/')}/auth/v1/.well-known/jwks.json"
SUPABASE_ISSUER = f"{SUPABASE_URL.rstrip('/')}/auth/v1"



@contextmanager
def context_manager(session_factory=Session):
    session = session_factory()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def extract_bearer_token(authorization: str | None) -> str:
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")

    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token.strip():
        raise HTTPException(status_code=401, detail="Invalid Authorization header")

    return token.strip()


def verify_supabase_jwt(token: str) -> dict:
    try:
        jwk_client = PyJWKClient(SUPABASE_JWKS_URL)
        signing_key = jwk_client.get_signing_key_from_jwt(token)

        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256", "ES256"],
            issuer=SUPABASE_ISSUER,
            options={
                "require": ["exp", "sub", "iss"],
                "verify_aud": False,
            },
        )
        return payload

    except InvalidTokenError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"JWT verification failed: {e}")


def get_user_id_and_email(authorization: str | None = Header(default=None)):
    print(f"URL:{SUPABASE_URL}, JWKS:{SUPABASE_JWKS_URL}, ISSUER:{SUPABASE_ISSUER}")
    token = extract_bearer_token(authorization)
    print(token)
    payload = verify_supabase_jwt(token)
    print(payload)

    user_metadata = payload.get("user_metadata") or {}
    supabase_user_id = payload.get("sub")
    email = payload.get("email")
    name = user_metadata.get("name")
    if not supabase_user_id:
        raise HTTPException(status_code=401, detail="User ID missing from token")
    if not email:
        raise HTTPException(status_code=401, detail="Email missing from token")

    with context_manager() as session:
        user = session.query(User).filter(User.email == email).first()

        if not user:
            user = User(
                email=email,
                supa_base_user_id=supabase_user_id,
                role="student",
                name=name
            )
            session.add(user)


        return user.id, user.email, supabase_user_id
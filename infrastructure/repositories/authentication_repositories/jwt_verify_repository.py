import base64
import os
from urllib.parse import urlparse
import jwt
import requests
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
from fastapi import HTTPException
from jwt import PyJWTError


NEON_BASE_URL = os.environ.get("NEON_BASE_URL")
NEON_JWKS_URL = f"{NEON_BASE_URL}/.well-known/jwks.json"
parsed = urlparse(NEON_BASE_URL)
ORIGIN = f"{parsed.scheme}://{parsed.netloc}"



def get_jwks():
    response = requests.get(NEON_JWKS_URL)
    response.raise_for_status()
    return response.json()
def get_signing_key(token, jwks):
    unverified_header = jwt.get_unverified_header(token)
    kid = unverified_header["kid"]
    for jwk in jwks["keys"]:
        if jwk["kid"] == kid:
            x = jwk["x"]
            public_key_bytes = base64.urlsafe_b64decode(x + "==")
            return Ed25519PublicKey.from_public_bytes(public_key_bytes)
    raise ValueError("Matching JWK not found")
def validate_neon_token(token: str):
    try:
        jwks = get_jwks()
        signing_key = get_signing_key(token, jwks)
        payload = jwt.decode(
            token, key=signing_key, algorithms=["EdDSA"], issuer=ORIGIN, audience=ORIGIN
        )
        return payload
    except PyJWTError as error:
        print("Token validation failed:", error)
        return HTTPException(status_code=401, detail="Invalid token")
    except Exception as error:
        print("Unexpected error:", error)
        return HTTPException(status_code=500, detail="Internal server error")
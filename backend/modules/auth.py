import httpx
import jwt
from fastapi import HTTPException
from modules.config import Config

_jwks_cache = None

async def _get_jwks():
    global _jwks_cache
    if _jwks_cache is None:
        if not Config.JWKS_URL:
            raise HTTPException(status_code=500, detail="Auth misconfigured: AZURE_TENANT_ID not set; cannot resolve JWKS_URL")
        async with httpx.AsyncClient() as client:
            r = await client.get(Config.JWKS_URL, timeout=10.0)
            r.raise_for_status()
            _jwks_cache = r.json()
    return _jwks_cache

async def verify_bearer_token(authorization: str = None):
    if not authorization:
        raise HTTPException(status_code=401, detail="Missing Authorization header")
    parts = authorization.split()
    if parts[0].lower() != "bearer" or len(parts) != 2:
        raise HTTPException(status_code=401, detail="Invalid Authorization header format")
    token = parts[1]
    # If JWKS is not configured (dev mode), decode without verification
    if not Config.JWKS_URL:
        try:
            claims = jwt.decode(token, options={"verify_signature": False})
            return claims
        except Exception:
            raise HTTPException(status_code=401, detail="Invalid token")

    jwks = await _get_jwks()
    try:
        unverified_header = jwt.get_unverified_header(token)
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid token header")
    kid = unverified_header.get("kid")
    key = None
    for k in jwks.get("keys", []):
        if k.get("kid") == kid:
            key = k
            break
    if not key:
        raise HTTPException(status_code=401, detail="Invalid token: unknown kid")
    try:
        claims = jwt.decode(token, options={"verify_signature": False})
        return claims
    except Exception as e:
        raise HTTPException(status_code=401, detail=f"Token validation error: {e}")

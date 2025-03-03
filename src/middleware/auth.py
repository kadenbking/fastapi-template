from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader
from starlette.status import HTTP_403_FORBIDDEN

from config import Settings

settings = Settings()
api_key_header = APIKeyHeader(name="X-API-Key")


class AuthMiddleware:
    async def validate_api_key(key: str = Security(api_key_header)):
        if key != settings.API_KEY:
            raise HTTPException(status_code=HTTP_403_FORBIDDEN, detail="Unable to validate API key")
        return None

from pydantic import BaseModel


class VersionResponse(BaseModel):
    version: str = "0000.00.00"

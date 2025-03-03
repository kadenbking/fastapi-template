from pydantic import BaseModel


class DefaultResponse(BaseModel):
    message: str = "Welcome to the PayTechGuide API!"

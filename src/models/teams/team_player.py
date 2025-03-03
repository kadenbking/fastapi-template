from pydantic import BaseModel


class TeamPlayer(BaseModel):
    team_id: str
    name: str
    number: str
    position: str

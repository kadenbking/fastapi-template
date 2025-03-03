from pydantic import BaseModel
from typing import Dict, List, Optional

from models.teams.team_player import TeamPlayer


class Team(BaseModel):
    team_id: str
    name: str
    nickname: str
    logo: Optional[str] = None
    players: List[TeamPlayer]
    sponsors: Optional[List[str]] = None

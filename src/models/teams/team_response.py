from pydantic import BaseModel
from typing import List

from models.teams.team import Team


class TeamResponse(BaseModel):
    teams: List[Team]

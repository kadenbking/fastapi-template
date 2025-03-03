from pydantic import BaseModel
from typing import List

from models.viewed_teams.viewed_teams import ViewedTeams


class ViewedTeamsList(BaseModel):
    viewed_teams: List[ViewedTeams]

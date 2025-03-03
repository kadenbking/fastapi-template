from datetime import datetime
from pydantic import BaseModel
from typing import List


class ViewedTeams(BaseModel):
    date_updated_utc: datetime
    team_ids: List[str]

from mysql.connector import Error
from pydantic import BaseModel, EmailStr, field_validator
from typing import List

from config import Settings
from db.connect import fetch_rows
from db.queries import GET_TEAM_IDS_BY_IDS_QUERY

settings = Settings()


class ViewedTeamsUpdateRequest(BaseModel):
    user_email: EmailStr
    team_ids: List[str]

    @field_validator("team_ids")
    def validate_team_ids(cls, team_ids):
        if not (1 <= len(team_ids) <= settings.VIEWED_TEAMS_LIMIT):
            raise ValueError(f"The 'team_ids' list must contain between 1 and {settings.VIEWED_TEAMS_LIMIT} teams.")

        placeholders = ", ".join(["%s"] * len(team_ids))
        query = GET_TEAM_IDS_BY_IDS_QUERY % placeholders

        try:
            rows = fetch_rows(query, tuple(team_ids))
            valid_ids = {row["team_id"] for row in rows}
        except Error as e:
            raise ValueError("Failed to validate 'team_ids' due to a database error.")

        invalid_ids = set(team_ids) - valid_ids
        if invalid_ids:
            raise ValueError(f"The following 'team_ids' are invalid: {', '.join(invalid_ids)}")

        return team_ids

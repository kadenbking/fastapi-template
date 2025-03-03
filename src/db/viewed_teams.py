import json
from datetime import datetime, timezone
from fastapi import HTTPException
from mysql.connector import Error
from typing import Any, Dict, List, Optional

from config import Settings
from db.connect import fetch_rows, insert_row
from db.queries import GET_VIEWED_TEAMS_QUERY, UPDATE_VIEWED_TEAMS_QUERY
from models.viewed_teams.viewed_teams import ViewedTeams
from models.viewed_teams.viewed_teams_request import ViewedTeamsUpdateRequest

settings = Settings()


def get_user_viewed_teams(user_email: str) -> List[ViewedTeams]:
    try:
        user_viewed_teams = _get_user_viewed_teams(user_email)
        if not user_viewed_teams:
            raise HTTPException(status_code=404, detail=f"No team_ids saved for user_email: {user_email}")

        return [_map_row_to_viewed_teams(row) for row in user_viewed_teams]
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))


def update_user_viewed_teams(viewed_teams_update_request: ViewedTeamsUpdateRequest) -> str:
    # Get current viewed teams from db
    current_viewed_teams = _get_user_viewed_teams(viewed_teams_update_request.user_email)

    # Add timestamps to new viewed teams
    new_viewed_team_json = [
        {"team_id": search, "timestamp": datetime.now().isoformat()} for search in viewed_teams_update_request.team_ids
    ]

    # Merge current (if any) and new viewed teams arrays
    if current_viewed_teams:
        current_viewed_team_json = [_map_row_to_team_json(row) for row in current_viewed_teams]
        combined_viewed_teams = current_viewed_team_json[0] + new_viewed_team_json
    else:
        combined_viewed_teams = new_viewed_team_json

    # Use a dictionary to filter out duplicates team_ids
    unique_viewed_teams = {}
    for team in combined_viewed_teams:
        unique_viewed_teams[team["team_id"]] = team

    # Sort the unique team_ids by timestamp and keep the most recent number defined in {settings.VIEWED_teamS_LIMIT}
    viewed_teams_limit = settings.VIEWED_TEAMS_LIMIT
    limited_teams = sorted(unique_viewed_teams.values(), key=lambda x: x["timestamp"], reverse=True)[
        :viewed_teams_limit
    ]

    # Parse viewed teams into json to update db record
    viewed_teams_json = json.dumps(limited_teams)
    date_updated = datetime.now()
    params = (
        viewed_teams_update_request.user_email,
        date_updated,
        viewed_teams_json,
    )

    try:
        insert_row(UPDATE_VIEWED_TEAMS_QUERY, params)
        return f"Most recent {len(limited_teams)} viewed team_ids saved successfully for user_email: {viewed_teams_update_request.user_email}"
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))


def _get_user_viewed_teams(user_email: str) -> List[Dict[str, Any]]:
    try:
        return fetch_rows(GET_VIEWED_TEAMS_QUERY, (user_email,))
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))


def _map_row_to_viewed_teams(row: Dict[str, Any]) -> ViewedTeams:
    teams = _parse_json(row.get("teams"), default=[])
    processed_fields = {
        "date_updated_utc": row.get("date_updated").replace(tzinfo=timezone.utc),
        "team_ids": [search["team_id"] for search in teams],
    }
    return ViewedTeams(**{**row, **processed_fields})


def _map_row_to_team_json(row: Dict[str, Any]) -> List[Dict[str, Any]]:
    return _parse_json(row.get("teams"), default=[])


def _parse_json(value: Optional[str], default=None) -> Any:
    if value:
        return json.loads(value)
    return default

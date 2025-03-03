import json
from fastapi import HTTPException
from mysql.connector import Error
from typing import Any, Dict, List, Optional, Tuple

from config import Settings
from db.connect import fetch_rows
from db.queries import GET_TEAMS_QUERY
from models.teams.team import Team
from models.teams.team_player import TeamPlayer

settings = Settings()


def get_filtered_teams(team_id: Optional[str]) -> List[Team]:
    query, params = _build_query(team_id)

    try:
        rows = fetch_rows(query, params)
        if not rows:
            raise HTTPException(status_code=404, detail=f"No team exists with team_id: {team_id}")

        return [_map_row_to_team(row) for row in rows]

    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))


def _build_query(team_id: Optional[str]) -> Tuple[str, Tuple]:
    query = GET_TEAMS_QUERY
    params = (team_id,) if team_id else ()
    if team_id:
        query += " WHERE p.team_id = %s"
    return query, params


def _map_row_to_team(row: Dict[str, Any]) -> Team:
    processed_fields = {
        "name": row.get("name") or row["nickname"],
        "logo": f"{settings.S3_BUCKET}/{row.get('logo')}",
        "sponsors": _parse_json(row.get("sponsors")),
        "players": [TeamPlayer(**detail) for detail in _parse_json(row.get("players"), [])],
    }

    return Team(**{**row, **processed_fields})


def _parse_json(value: Optional[str], default=None) -> Any:
    if value:
        return json.loads(value)
    return default

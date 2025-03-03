from fastapi import FastAPI, Depends, Response
from pydantic import EmailStr
from starlette.middleware.cors import CORSMiddleware
from starlette.status import HTTP_200_OK
from typing import Optional

from config import Settings
from middleware.auth import AuthMiddleware
from middleware.exception import ExceptionHandlerMiddleware
from models.teams.team_response import TeamResponse
from models.viewed_teams.viewed_teams_list_response import ViewedTeamsList
from models.viewed_teams.viewed_teams_request import ViewedTeamsUpdateRequest
from models.shared.default_response import DefaultResponse
from models.shared.version_response import VersionResponse
from db.teams import get_filtered_teams
from db.viewed_teams import get_user_viewed_teams, update_user_viewed_teams

settings = Settings()

# Setup FastAPI app
docs_url = "/docs" if settings.APP_ENV == "dev" else None
app = FastAPI(
    title="PTG_API",
    version=settings.APP_VERSION,
    docs_url=docs_url,
)

# Enable CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_credentials=False,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Enable Custom Exception Handling Middleware
app.add_middleware(ExceptionHandlerMiddleware)


# Routes
@app.get("/", dependencies=[Depends(AuthMiddleware.validate_api_key)])
def get_index() -> DefaultResponse:
    """
    Responds with a welcome message at the root path of the application.

    This synchronous endpoint is the default route for the application and is
    accessed via a GET request. When invoked, it returns a JSON object with a
    greeting message, indicating that the application is successfully running.

    Returns:
        dict: A JSON object containing a welcome message to the Application.

    Example usage:
        curl http://localhost:80/
    """
    return DefaultResponse()


@app.get("/health", dependencies=[])
def get_health() -> DefaultResponse:
    """
    Responds with a an empty 200 HttpStatusResponse to affirm app health.

    This synchronous endpoint is the default route for the application's health
    checks. This is the only route that is not protected with an API Key validation.

    Returns:
        HttpStatus 200 OK

    Example usage:
        curl http://localhost:00/health
    """
    return Response(status_code=HTTP_200_OK)


@app.get("/status", dependencies=[Depends(AuthMiddleware.validate_api_key)])
def get_api_status() -> VersionResponse:
    """
    Retrieves the current version (date of last update) of the API.

    This synchronous endpoint is a quick way to check the API version (which is the date of the
    most recent API update). It returns a JSON object containing the version number.
    This can be useful for debugging, logging, or ensuring compatibility with client applications.

    Returns:
       dict: A JSON object containing the API version number (date of last API update).

    Example usage:
    curl http://localhost:80/status
    """
    return VersionResponse(version=settings.APP_VERSION)


# teamS
@app.get("/teams", dependencies=[Depends(AuthMiddleware.validate_api_key)])
def get_teams(team_id: Optional[str] = None) -> TeamResponse:
    """
    Responds with a list of team information.

    This synchronous endpoint is the default route for retrieving team information.
    team ids retrieved by this endpoint can then be used as query parameters to
    filter the response.

    Returns:
        dict: A JSON object containing a list of team information.

    Example usages:
        curl http://localhost:80/teams
        curl http://localhost:80/teams?team_id={team_id}
    """
    return TeamResponse(teams=get_filtered_teams(team_id))


# VIEWED TEAMS
@app.get("/teams/viewed/{user_email}", dependencies=[Depends(AuthMiddleware.validate_api_key)])
def get_viewed_teams(user_email: EmailStr) -> ViewedTeamsList:
    """
    Responds with a list of saved viewed teams for the requested user_email.

    This synchronous endpoint is the default route for retrieving user viewed team_ids.
    The list of team_ids retrieved by this endpoint belong to the user_email in the request.

    Returns:
        dict: A JSON object containing a list of viewed team_ids.

    Example usage:
        curl http://localhost:80/teams/viewed/test@example.com
    """
    return ViewedTeamsList(viewed_teams=get_user_viewed_teams(user_email))


@app.post("/teams/viewed", dependencies=[Depends(AuthMiddleware.validate_api_key)])
def update_viewed_teams(viewed_teams_update_request: ViewedTeamsUpdateRequest) -> DefaultResponse:
    """
    Responds with a status message indicating the update operation's success.

    This synchronous endpoint is the default route for incrementally updating user viewed teams
    for a user_email. This operation is only meant for adding or updating a user's most recent viewed team_ids.

    Returns:
        dict: A JSON object containing a status message of the operation.

    Example usages:
        curl -X POST http://localhost:80/teams/viewed -H "Content-Type: application/json" -d '{"domain": "local", "user_email": "test@example.com", "team_ids": [{team_id}]}'
    """
    return DefaultResponse(message=update_user_viewed_teams(viewed_teams_update_request))

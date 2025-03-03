# fastapi-template

---

## Table of Contents

- [Project Organization](#project-organization)
- [Local Development](#local-development)
  - [Pipenv Virtual Environment](#pipenv-virtual-environment)
  - [Run the API Server](#run-the-api-server)
  - [Debug the API Server](#debug-the-api-server)
- [Deployment](#deployment)

---

## Project Organization

---

```
.
├── .env
├── .env.example
├── api.rest
├── docker-compose.yml
├── README.md
├── .github
│   └── workflows
│       └── ...                             <- Github Actions
└── src                                     <- Modules for deployable API
    ├── Dockerfile
    ├── Pipfile
    ├── Pipfile.lock
    ├── requirements.txt
    ├── config.py                           <- Dotenv configuration
    ├── api
    │   └── server.py                       <- API entrypoint
    ├── db
    │   ├── connect.py                      <- Connection and Query methods for AWS MySQL DB
    │   ├── teams.py                        <- Data Layer for Teams Operations
    │   ├── viewed_teams.py                 <- Data Layer for Viewed Teams Operations
    │   └── queries.py                      <- MySQL string queries
    ├── middleware
    │   ├── auth.py                         <- API Key validation for FastAPI endpoints
    │   └── exception.py                    <- Exception Handling for FastAPI endpoints
    └── models
        ├── teams
        │   └── ...                         <- Pydantic classes for teams object specification
        ├── viewed_teams
        │   └── ...                         <- Pydantic classes for viewed teams object specification
        └── shared
            └── ...                         <- Pydantic classes for shared object specification
```

---

## Local Development

---

### Pipenv Virtual Environment

This project's package and environment management is controlled with [Pipenv](https://pipenv.pypa.io/en/latest/). See the official [documentation](https://pipenv.pypa.io/en/latest/) to learn more.

---

### Run the API Server

### Run from the Command Line

To start the API server locally from the command line, run:

```bash
$ cd fastapi-template/src
$ uvicorn api.server:app --host 0.0.0.0 --port 80
```

### Run from Docker container

To start the API server locally from a docker container, run:

```bash
$ cd fastapi-template
$ docker-compose up -d
```

---

### Debug the API Server

You may also use VsCode's built in debugger to run the server. Just select 'FastAPI-Template' from the dropdown and click the green play button.
You may also use rest client to test / debug the api. Open the rest client file in the root of the project and run the requests.

---

## Deployment

`TODO`

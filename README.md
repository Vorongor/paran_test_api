# 🚀 User Profile & Auth API (FastAPI)

A high-performance, asynchronous REST API system built with **FastAPI** and *
*PostgreSQL**. The project implements a secure authentication flow and a
dedicated PDF generation service, adhering to a clean, layered architecture.

# 🛠 Tech Stack

- Framework: FastAPI
- Database: PostgreSQL
- ORM: SQLAlchemy 2.0 (Async)
- Migrations: Alembic
- Validation: Pydantic v2
- Security: PyJWT, bcrypt
- Deployment: Docker & Docker Compose
- pdf2: Create user profile file

# Project structure

```
/
├── auth_service/                # Auth App Dir
│   ├── config/                  # Contain settings and dependencies
│   │   ├── dependencies.py      # Core dependencies (get_settings, get_jwt_manager)
│   │   ├── logging_config.py    # Logger setup
│   │   └── settings.py          # All settings entities
│   ├── crud/                    # Database logic
│   │   ├── profile.py           # Retrieve prifile logic
│   │   └── user.py              # User auth logic
│   ├── database/                # Database logic
│   │   ├── migrations/          # Alembic data
│   │   │   ├── versions/        # Migrations files
│   │   │   └── env.py           # Alembic configuration
│   │   ├── models/              # App models
│   │   │   └── user.py          # User and RefreshTOken models
│   │   ├── base.py              # Initialization of base model
│   │   └── engine.py            # DB engine and session, get_db dependency
│   ├── exceptions/              # Custom exceptions
│   │   ├── user.py              # User custom exceptions
│   │   └── security.py          # Security custom exceptions
│   ├── routers/                 # App routers
│   │   ├── api.py               # Router version controler
│   │   ├── profile.py           # Profile endpoints
│   │   └── user.py              # Auth endpoints
│   ├── schemas/                 # Pydentic schemas
│   │   └── user.py              # Auth schemas
│   ├── security/                # App security ligic
│   │   ├── interfaces.py        # JWT manager interface
│   │   ├── password.py          # Password processing helpers
│   │   ├── token_manager.py     # JWT manager
│   │   └── utils.py             # get_current_user dependency (retrieve auth user for protected endpoints)
│   ├── validators/              # Service validators
│   │   └── password.py          # Password valodator
│   ├── Dockerfile               # Auth App image instruction
│   ├── pyproject.toml           # Auth App configuration
│   ├── alembic.ini              # Auth App configuration
│   ├── requirements.txt         
│   └── main.py                  # App entry point
├── pdf_service/                 # PDF App Dir
│   ├── config/                  # Contain settings and dependencies
│   │   ├── dependencies.py      # core dependencies (get_settings, get_jwt_manager)
│   │   ├── logging_config.py    # Logger setup
│   │   └── settings.py          # All settings entities
│   ├── crud/                    # Database logic
│   │   └── profile.py           # PDF profile logic logic
│   ├── routers/                 # App routers
│   │   └── pdf_router.py              
│   ├── schemas/                 # Pydentic schemas
│   │   └── profile.py           # Profile schemas
│   ├── security/                # Contain settings and dependencies
│   │   ├── interfaces.py        # JWT manager interface
│   │   ├── token_manager.py     # JWT manager
│   │   └── utils.py             # get_current_user dependency (retrieve auth user for protected endpoints)
│   ├── services/                # App services
│   │   └── profile/             # PDF Generation Service
│   ├── storage/                 # Contain settings and dependencies
│   │   ├── interfaces.py        # S3 and SQS managers interfaces
│   │   ├── s3.py                # S3 manager
│   │   ├── sqs.py               # SQS manager
│   │   └── exeptions.py         # S3 and SQS exceptions
│   ├── Dockerfile               # PDF App image instruction
│   ├── pyproject.toml           # PDF App configuration
│   ├── init-aws.sh              # Initial command for queue and storage
│   ├── worker.py                # Script for runnig pdf_saver worker 
│   ├── requirements.txt         
│   └── pdf_main.py              # App entry point
├── tests/                       # App tests
├── compose.yml                  # Main runner
├── docker-compose.override.yml  # Pytest suite
├── pyproject.toml               # App configuration
├── .env.sample                  # App envinroment variables
└── requirements-dev.txt         # Main dev requirements
```

# Core Dependencies

The project utilizes FastAPI's Depends for clean Dependency Injection:
Auth Service
- **get_settings**: Returns the current configuration 
- **get_db**: Provides an asynchronous bd session - based on env and settings.
- **get_jwt_manager**: Returns the JWT handler based on an interface.
- **get_current_user**: Secures endpoints by validating the bearer token.


# Run project

1. Prerequisites: Docker and Docker Compose.
2. Copy .env.sample into .env and populate data.
3. Launch the Project
   Run the following command to build the image and start the PostgreSQL
   database and API:

```Bash
  docker compose up --build
```

API Documentation: http://localhost:8000/docs (Swagger UI)

🧪 Testing
The project includes a pytest suite configured to run in an isolated
environment via a Docker override.

**Don't forget build before testing**


```Bash
  # Run infrastructure
  docker compose up -d project_db localstack

  # Run Auth test
  docker compose run --rm auth_tester

  # Run PDF test
  docker compose run --rm pdf_tester
  # Run end-to-end test inside the docker environment
  docker compose --profile e2e_test up --build --attach e2e_tester
```
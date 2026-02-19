Технічне завдання.

Test Task — Trainee Backend Developer

Build a small project with a REST API and a PostgreSQL database.

API (FastAPI)
- REST API with async endpoints
- Clients can register (name, surname, email, date of birth, password) and login (email, password) - Done
- After registration/login, users have one endpoint to download a PDF containing their profile data

Database
- PostgreSQL - Done

Must have
- Docker + docker-compose as the main project runner - Done
- One command to start the project (docker compose up --build) - Done
- Uploaded to GitHub with a clear README
- Clear and expandable project structure (e.g. routers, models, schemas, crud separated)
- SQLAlchemy 2.0 with async support (asyncpg driver) - Done
- Alembic for migrations - Done
- Connection pooling
- At least one pytest test (any scenario)

Nice to have
- Split auth and PDF generation into 2 independent services that communicate only via JWT (no shared DB)
- docker-compose.override.yml for running the pytest suite in isolation
- Split requirements.txt into requirements.txt and requirements-dev.txt (or requirements-test.txt)
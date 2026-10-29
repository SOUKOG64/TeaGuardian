# TeaGuardian

TeaGuardian is a simple tea brewing assistant made as a student project with a FastAPI backend and a Kivy desktop client.

## Project structure

- `server/app` — FastAPI backend, SQLAlchemy models, repositories, services, routers
- `client` — Kivy desktop application
- `database.py` and `main.py` — compatibility files from earlier prototype stages

## Quick start on Windows

1. Create a virtual environment:
   py -m venv .venv

2. Activate it:
   .\.venv\Scripts\Activate.ps1

3. Install dependencies:
   python -m pip install --upgrade pip
   pip install -r requirements.txt

4. Start the API:
   start_backend.bat

5. Start the desktop client:
   start_client.bat

6. Open Swagger UI:
   http://127.0.0.1:8000/docs

## Main features

- Registration and login with JWT tokens
- Protected recipe CRUD for the current user
- Search by recipe name
- Tea brewing timer for selected recipe
- SQLite database with seeded tea types

## Notes

- The backend listens on http://127.0.0.1:8000
- The client calls the API using the local backend URL
- If port 8000 is busy, run the server with a different port manually:
  cd server
  python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8001

## Basic validation flow

1. Open the Swagger page
2. Register a new user
3. Log in via the auth endpoint
4. Create a recipe
5. Load the recipe list in Kivy
6. Run the tea timer for the selected recipe

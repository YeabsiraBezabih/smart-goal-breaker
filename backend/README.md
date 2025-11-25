# Smart Goal Breaker - Backend

FastAPI backend for the Smart Goal Breaker application with Gemini AI integration.

## Setup

1. **Create a virtual environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and add your:
   - PostgreSQL database URL
   - Gemini API key (get it from https://makersuite.google.com/app/apikey)

4. **Start the Database (Docker):**
   ```bash
   # From the project root (one level up)
   docker-compose up -d
   ```
   This starts a PostgreSQL instance on port 5432.

## Running the Server

```bash
uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

- `POST /api/goals` - Create a new goal and generate tasks
- `GET /api/goals` - List all goals with tasks
- `GET /api/goals/{goal_id}` - Get a specific goal
- `DELETE /api/goals/{goal_id}` - Delete a goal

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application
│   ├── database.py      # Database configuration
│   ├── models.py        # SQLAlchemy models
│   ├── schemas.py       # Pydantic schemas
│   └── ai_service.py    # Gemini AI integration
├── requirements.txt
├── .env.example
└── .gitignore
```

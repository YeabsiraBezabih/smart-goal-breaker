"""FastAPI main application."""

from fastapi import FastAPI, Depends, HTTPException, Request, Response
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from .database import engine, get_db, Base
from .models import Goal, Task
from .schemas import GoalCreate, GoalResponse
from .ai_service import break_down_goal
from .session import get_session_id, set_session_cookie

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Smart Goal Breaker API",
    description="AI-powered goal breakdown service",
    version="1.0.0"
)

# Configure CORS for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",  # Local development
        "https://*.vercel.app",  # Vercel deployments
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    """Root endpoint."""
    return {
        "message": "Smart Goal Breaker API",
        "version": "1.0.0",
        "endpoints": {
            "create_goal": "POST /api/goals",
            "list_goals": "GET /api/goals",
            "get_goal": "GET /api/goals/{goal_id}"
        }
    }


@app.post("/api/goals", response_model=GoalResponse, status_code=201)
def create_goal(
    goal_data: GoalCreate,
    request: Request,
    response: Response,
    db: Session = Depends(get_db)
):
    """
    Create a new goal and generate actionable tasks using AI.
    
    Args:
        goal_data: Goal creation data with goal_text
        request: FastAPI request (for session)
        response: FastAPI response (for setting cookies)
        db: Database session
        
    Returns:
        GoalResponse with generated tasks and complexity score
    """
    try:
        # Get or create session ID
        session_id = get_session_id(request)
        set_session_cookie(response, session_id)
        
        # Use AI to break down the goal
        ai_result = break_down_goal(goal_data.goal_text)
        
        # Create goal in database
        db_goal = Goal(
            user_id=session_id,
            goal_text=goal_data.goal_text,
            complexity_score=ai_result["complexity_score"]
        )
        db.add(db_goal)
        db.flush()  # Get the goal ID without committing
        
        # Create tasks in database
        for idx, task_text in enumerate(ai_result["tasks"], start=1):
            db_task = Task(
                goal_id=db_goal.id,
                task_text=task_text,
                order=idx
            )
            db.add(db_task)
        
        # Commit all changes
        db.commit()
        db.refresh(db_goal)
        
        return db_goal
        
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating goal: {str(e)}")


@app.get("/api/goals", response_model=List[GoalResponse])
def list_goals(
    request: Request,
    response: Response,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    List all goals with their tasks for the current user.
    
    Args:
        request: FastAPI request (for session)
        response: FastAPI response (for setting cookies)
        skip: Number of records to skip
        limit: Maximum number of records to return
        db: Database session
        
    Returns:
        List of goals with tasks for current user
    """
    # Get or create session ID
    session_id = get_session_id(request)
    set_session_cookie(response, session_id)
    
    # Filter by user_id
    goals = db.query(Goal).filter(Goal.user_id == session_id).order_by(Goal.created_at.desc()).offset(skip).limit(limit).all()
    return goals


@app.get("/api/goals/{goal_id}", response_model=GoalResponse)
def get_goal(goal_id: int, request: Request, db: Session = Depends(get_db)):
    """
    Get a specific goal with its tasks (ownership verified).
    
    Args:
        goal_id: Goal ID
        request: FastAPI request (for session)
        db: Database session
        
    Returns:
        Goal with tasks
    """
    session_id = get_session_id(request)
    goal = db.query(Goal).filter(Goal.id == goal_id, Goal.user_id == session_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    return goal


@app.delete("/api/goals/{goal_id}")
def delete_goal(goal_id: int, request: Request, db: Session = Depends(get_db)):
    """
    Delete a specific goal and its tasks (ownership verified).
    
    Args:
        goal_id: Goal ID
        request: FastAPI request (for session)
        db: Database session
        
    Returns:
        Success message
    """
    session_id = get_session_id(request)
    goal = db.query(Goal).filter(Goal.id == goal_id, Goal.user_id == session_id).first()
    if not goal:
        raise HTTPException(status_code=404, detail="Goal not found")
    
    db.delete(goal)
    db.commit()
    return {"message": "Goal deleted successfully"}

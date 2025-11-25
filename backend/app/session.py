"""Session management for multi-user support."""

import uuid
from typing import Optional
from fastapi import Request, Response


def get_session_id(request: Request) -> str:
    """
    Get or generate a session ID from cookies.
    
    Args:
        request: FastAPI request object
        
    Returns:
        Session ID string
    """
    session_id = request.cookies.get("session_id")
    if not session_id:
        session_id = str(uuid.uuid4())
    return session_id


def set_session_cookie(response: Response, session_id: str) -> None:
    """
    Set the session ID cookie in the response.
    
    Args:
        response: FastAPI response object
        session_id: Session ID to set
    """
    response.set_cookie(
        key="session_id",
        value=session_id,
        httponly=True,
        max_age=60 * 60 * 24 * 365,  # 1 year
        samesite="none",  # Required for cross-origin requests (Vercel/Render)
        secure=True  # Required for cross-origin requests
    )

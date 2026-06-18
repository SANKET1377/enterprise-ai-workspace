
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.security.dependencies import (
    get_current_user
)

from app.database.chat_crud import (
    save_chat
)

from app.database.crud import (
    get_user_by_username
)
from app.database.crud import (
    get_user_by_email,
    get_user_by_username,
    create_user
)

from app.schemas.user import (
    UserCreate,
    UserResponse,
    UserLogin,
    TokenResponse
)

from app.security.auth import (
    hash_password,
    verify_password
)

from app.security.jwt_handler import (
    create_access_token
)
from app.security.dependencies import (
    get_current_user
)
from app.schemas.chat import (
    ChatRequest,
    ChatResponse
)

from app.services.gemini_service import (
    ask_gemini
)

app = FastAPI(
    title="Enterprise AI Workspace",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "status": "running",
        "project": "Enterprise AI Workspace"
    }

@app.get("/health")
def health():
    return {
        "status": "healthy"
    }

@app.post(
    "/register",
    response_model=UserResponse
)
def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    existing_user = get_user_by_email(
        db,
        user.email
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    hashed_password = hash_password(
        user.password
    )

    new_user = create_user(
        db=db,
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    return new_user

@app.post(
    "/login",
    response_model=TokenResponse
)
def login(
    user: UserLogin,
    db: Session = Depends(get_db)
):
    db_user = get_user_by_username(
        db,
        user.username
    )

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    if not verify_password(
        user.password,
        db_user.hashed_password
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid credentials"
        )

    token = create_access_token(
        {
            "sub": db_user.username
        }
    )

    return {
        "access_token": token,
        "token_type": "bearer"
    }

@app.get("/me")
def get_me(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user = get_user_by_username(
        db,
        current_user
    )

    return {
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "is_active": user.is_active
    }
    
@app.post(
    "/chat",
    response_model=ChatResponse
)
def chat(
    request: ChatRequest,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user = get_user_by_username(
        db,
        current_user
    )

    answer = ask_gemini(
        request.message
    )

    save_chat(
        db=db,
        user_id=user.id,
        message=request.message,
        response=answer
    )

    return {
        "response": answer
    }
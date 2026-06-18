
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db

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


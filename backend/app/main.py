
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.connection import get_db
from app.security.dependencies import (
    get_current_user
)
from fastapi import UploadFile, File

from app.database.document_crud import (
    save_document
)

import shutil
import os
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
from app.database.chat_crud import (
    save_chat,
    get_user_chats
)

from app.schemas.chat_history import (
    ChatHistoryResponse
)

from typing import List



app = FastAPI(
    title="Enterprise AI Workspace",
    version="1.0.0"
)
from app.database.document_crud import (
    save_document,
    get_latest_document
)

from app.schemas.document_chat import (
    DocumentQuestion
)

from app.rag.pdf_loader import (
    extract_text_from_pdf
)

from app.rag.chunker import (
    chunk_text
)

from app.rag.vector_store import (
    create_vector_store
)

from app.rag.rag_service import (
    build_rag_prompt
)

from app.database.document_crud import (
    save_document,
    get_latest_document,
    get_user_documents
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
    
@app.get(
    "/chat-history",
    response_model=List[ChatHistoryResponse]
)
def chat_history(
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user = get_user_by_username(
        db,
        current_user
    )

    return get_user_chats(
        db,
        user.id
    )
    
@app.post("/upload-pdf")
def upload_pdf(
    file: UploadFile = File(...),
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user = get_user_by_username(
        db,
        current_user
    )

    os.makedirs(
        "uploads",
        exist_ok=True
    )

    file_path = f"uploads/{file.filename}"

    with open(
        file_path,
        "wb"
    ) as buffer:

        shutil.copyfileobj(
            file.file,
            buffer
        )

    save_document(
        db=db,
        user_id=user.id,
        filename=file.filename,
        file_path=file_path
    )

    return {
        "message": "PDF uploaded successfully",
        "filename": file.filename
    }
    
@app.post("/ask-document")
def ask_document(
    request: DocumentQuestion,
    current_user: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):

    user = get_user_by_username(
        db,
        current_user
    )

    documents = get_user_documents(
        db,
        user.id
    )

    if not documents:
        raise HTTPException(
            status_code=404,
            detail="No documents found"
        )

    all_chunks = []

    for document in documents:

        text = extract_text_from_pdf(
            document.file_path
        )

        chunks = chunk_text(
            text,
            chunk_size=500
        )

        all_chunks.extend(
            chunks
        )

    index, embeddings = create_vector_store(
        all_chunks
    )

    prompt = build_rag_prompt(
        request.question,
        index,
        all_chunks
    )

    answer = ask_gemini(
        prompt
    )

    return {
        "documents_searched": len(documents),
        "answer": answer
    }
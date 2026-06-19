from sqlalchemy.orm import Session
from app.database.models import User


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()


def create_user(
    db: Session,
    username: str,
    email: str,
    hashed_password: str
):
    user = User(
        username=username,
        email=email,
        hashed_password=hashed_password
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user

def get_user_by_username(
    db: Session,
    username: str
):
    return (
        db.query(User)
        .filter(User.username == username)
        .first()
    )
from app.database.models import (
    User,
    Document
)


def save_document(
    db: Session,
    user_id: int,
    filename: str,
    file_path: str,
    index_path: str = ""
):

    document = Document(
        user_id=user_id,
        filename=filename,
        file_path=file_path,
        index_path=index_path
    )

    db.add(document)

    db.commit()

    db.refresh(document)

    return document


def get_user_documents(
    db: Session,
    user_id: int
):

    return (
        db.query(Document)
        .filter(
            Document.user_id == user_id
        )
        .all()
    )


def update_document_index(
    db: Session,
    document_id: int,
    index_path: str
):

    document = (
        db.query(Document)
        .filter(
            Document.id == document_id
        )
        .first()
    )

    document.index_path = index_path

    db.commit()

    db.refresh(document)

    return document
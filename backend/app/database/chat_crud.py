from sqlalchemy.orm import Session

from app.database.models import ChatMessage


def save_chat(
    db: Session,
    user_id: int,
    message: str,
    response: str
):

    chat = ChatMessage(
        user_id=user_id,
        message=message,
        response=response
    )

    db.add(chat)
    db.commit()
    db.refresh(chat)

    return chat
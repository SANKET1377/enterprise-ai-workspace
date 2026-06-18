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

def get_user_chats(
    db: Session,
    user_id: int
):
    return (
        db.query(ChatMessage)
        .filter(
            ChatMessage.user_id == user_id
        )
        .order_by(
            ChatMessage.created_at.desc()
        )
        .all()
    )
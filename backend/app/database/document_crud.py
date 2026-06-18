from app.database.models import Document


def save_document(
    db,
    user_id,
    filename,
    file_path
):

    document = Document(
        user_id=user_id,
        filename=filename,
        file_path=file_path
    )

    db.add(document)
    db.commit()
    db.refresh(document)

    return document
def get_latest_document(
    db,
    user_id
):
    return (
        db.query(Document)
        .filter(
            Document.user_id == user_id
        )
        .order_by(
            Document.created_at.desc()
        )
        .first()
    )
    
def get_user_documents(
    db,
    user_id
):
    return (
        db.query(Document)
        .filter(
            Document.user_id == user_id
        )
        .all()
    )
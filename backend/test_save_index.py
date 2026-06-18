from app.rag.pdf_loader import (
    extract_text_from_pdf
)

from app.rag.chunker import (
    chunk_text
)

from app.rag.vector_store import (
    create_and_save_index
)

text = extract_text_from_pdf(
    "sample.pdf"
)

chunks = chunk_text(
    text
)

create_and_save_index(
    chunks,
    user_id=1
)

print("Index saved successfully!")
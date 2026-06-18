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

from app.services.gemini_service import (
    ask_gemini
)

text = extract_text_from_pdf(
    "sample.pdf"
)

chunks = chunk_text(
    text,
    chunk_size=200
)

index, embeddings = create_vector_store(
    chunks
)

prompt = build_rag_prompt(
    "What table exists in the document?",
    index,
    chunks
)

response = ask_gemini(
    prompt
)

print(response)
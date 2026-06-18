from app.rag.pdf_loader import (
    extract_text_from_pdf
)

from app.rag.chunker import (
    chunk_text
)

from app.rag.vector_store import (
    create_vector_store
)

from app.rag.retrieval import (
    search_chunks
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

results = search_chunks(
    "table information",
    index,
    chunks
)

print(results)
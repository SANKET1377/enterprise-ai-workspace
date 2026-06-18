from app.rag.vector_store import (
    load_index
)

index, chunks = load_index(
    1
)

print(
    "Chunks loaded:",
    len(chunks)
)
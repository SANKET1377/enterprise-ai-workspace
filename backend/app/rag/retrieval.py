import numpy as np

from app.rag.vector_store import (
    model
)


def search_chunks(
    query,
    index,
    chunks,
    k=3
):

    query_embedding = model.encode(
        [query]
    )

    distances, indices = index.search(
        np.array(
            query_embedding,
            dtype="float32"
        ),
        k
    )

    results = []

    for idx in indices[0]:
        results.append(
            chunks[idx]
        )

    return results
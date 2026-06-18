import faiss
import pickle
import numpy as np
import os

from sentence_transformers import (
    SentenceTransformer
)

model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


def create_and_save_index(
    chunks,
    user_id
):

    embeddings = model.encode(
        chunks
    )

    dimension = embeddings.shape[1]

    index = faiss.IndexFlatL2(
        dimension
    )

    index.add(
        np.array(
            embeddings,
            dtype="float32"
        )
    )
    os.makedirs(
    "vector_store",
    exist_ok=True
)

    faiss.write_index(
        index,
        f"vector_store/{user_id}.index"
    )

    with open(
        f"vector_store/{user_id}_chunks.pkl",
        "wb"
    ) as f:

        pickle.dump(
            chunks,
            f
        )


def load_index(
    user_id
):

    index = faiss.read_index(
        f"vector_store/{user_id}.index"
    )

    with open(
        f"vector_store/{user_id}_chunks.pkl",
        "rb"
    ) as f:

        chunks = pickle.load(f)

    return index, chunks
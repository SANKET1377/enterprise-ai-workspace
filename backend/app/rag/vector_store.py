import faiss
import pickle
import numpy as np
import os

model = None


def get_model():

    global model

    if model is None:

        from sentence_transformers import (
            SentenceTransformer
        )

        model = SentenceTransformer(
            "all-MiniLM-L6-v2"
        )

    return model


def create_and_save_index(
    chunks,
    document_id
):

    embeddings = get_model().encode(
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

    index_path = (
        f"vector_store/doc_{document_id}.index"
    )

    chunks_path = (
        f"vector_store/doc_{document_id}_chunks.pkl"
    )

    faiss.write_index(
        index,
        index_path
    )

    with open(
        chunks_path,
        "wb"
    ) as f:

        pickle.dump(
            chunks,
            f
        )

    return index_path


def load_index(
    document_id
):

    index = faiss.read_index(
        f"vector_store/doc_{document_id}.index"
    )

    with open(
        f"vector_store/doc_{document_id}_chunks.pkl",
        "rb"
    ) as f:

        chunks = pickle.load(f)

    return index, chunks
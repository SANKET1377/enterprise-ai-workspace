from app.rag.retrieval import search_chunks


def build_rag_prompt(
    question,
    index,
    chunks
):

    relevant_chunks = search_chunks(
        question,
        index,
        chunks,
        k=3
    )

    context = "\n\n".join(
        relevant_chunks
    )

    prompt = f"""
Answer the question only using the provided context.

Context:
{context}

Question:
{question}
"""

    return prompt
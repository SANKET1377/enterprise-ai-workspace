from app.rag.pdf_loader import (
    extract_text_from_pdf
)

from app.rag.chunker import (
    chunk_text
)

text = extract_text_from_pdf(
    "sample.pdf"
)

chunks = chunk_text(
    text,
    chunk_size=200
)

print("TOTAL CHUNKS:", len(chunks))

for i, chunk in enumerate(chunks):
    print("\n")
    print("=" * 50)
    print("CHUNK", i + 1)
    print("=" * 50)
    print(chunk)
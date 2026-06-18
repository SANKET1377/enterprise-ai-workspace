from app.rag.pdf_loader import (
    extract_text_from_pdf
)

text = extract_text_from_pdf(
    "sample.pdf"
)

print(text[:1000])
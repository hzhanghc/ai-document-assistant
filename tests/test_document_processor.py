from app.document_processor import (
    extract_text_from_pdf,
    create_chunks
)


pdf_path = "data/documents/test.pdf"

pages = extract_text_from_pdf(pdf_path)

print(f"Pages extracted: {len(pages)}")

chunks = create_chunks(pages)

print(f"Chunks created: {len(chunks)}")

for index, chunk in enumerate(chunks[:5], start=1):
    print(f"\n--- Chunk {index} ---")
    print(f"Page: {chunk['page']}")
    print(chunk["text"][:500])
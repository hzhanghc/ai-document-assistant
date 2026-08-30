from app.document_processor import (
    extract_text_from_pdf,
    create_chunks
)

from app.embeddings import generate_embeddings
from app.vector_store import VectorStore


PDF_PATH = "data/documents/test.pdf"


# 1. Extract PDF text
pages = extract_text_from_pdf(PDF_PATH)

print(f"Pages extracted: {len(pages)}")


# 2. Create chunks
chunks = create_chunks(pages)

print(f"Chunks created: {len(chunks)}")


# 3. Generate embeddings
texts = [chunk["text"] for chunk in chunks]

embeddings = generate_embeddings(texts)

print(f"Embeddings generated: {len(embeddings)}")


# 4. Prepare metadata
metadatas = [
    {
        "page": chunk["page"],
        "source": "Understanding Deep Learning"
    }
    for chunk in chunks
]


# 5. Create unique IDs
ids = [
    f"chunk_{index}"
    for index in range(len(chunks))
]


# 6. Create vector store
vector_store = VectorStore()

vector_store.reset()

# 7. Add everything to ChromaDB
vector_store.add_documents(
    documents=texts,
    embeddings=embeddings,
    metadatas=metadatas,
    ids=ids
)


print(
    f"Documents stored in ChromaDB: "
    f"{vector_store.count()}"
)
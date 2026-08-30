from app.embeddings import generate_embeddings


texts = [
    "Supervised learning uses labeled training data.",
    "Neural networks can learn complex patterns.",
    "The weather is sunny today."
]


embeddings = generate_embeddings(texts)

print(f"Number of embeddings: {len(embeddings)}")
print(f"Embedding dimensions: {len(embeddings[0])}")

for index, embedding in enumerate(embeddings):
    print(
        f"Text {index + 1}: "
        f"{len(embedding)} dimensions"
    )
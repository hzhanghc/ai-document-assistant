from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Generate vector embeddings for a list of text documents.

    Args:
        texts: Texts to encode.

    Returns:
        List of embedding vectors.
    """

    embeddings = model.encode(
        texts,
        show_progress_bar=True
    )

    return embeddings.tolist()
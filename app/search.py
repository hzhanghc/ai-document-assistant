from app.embeddings import generate_embeddings
from app.vector_store import VectorStore


# ============================================================
# SEARCH CONFIGURATION
# ============================================================

DEFAULT_N_RESULTS = 2
DEFAULT_MAX_DISTANCE = 1.35

# Retrieve more candidates from ChromaDB
# before re-ranking them.
CANDIDATE_RESULTS = 10


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def normalize_text(text: str) -> str:
    """
    Normalize text for lexical matching.
    """

    return (
        text.lower()
        .replace("-", " ")
        .replace("_", " ")
        .replace("'", "")
    )


# ============================================================
# LEXICAL RELEVANCE
# ============================================================

def lexical_score(
    query: str,
    document: str
) -> int:
    """
    Calculate lexical overlap between a query
    and a retrieved document.

    This complements semantic similarity by
    rewarding documents that contain terminology
    explicitly present in the user's question.
    """

    query_text = normalize_text(
        query
    )

    document_text = normalize_text(
        document
    )

    query_words = {
        word
        for word in query_text.split()
        if len(word) > 2
    }

    document_words = {
        word
        for word in document_text.split()
        if len(word) > 2
    }

    return len(
        query_words.intersection(
            document_words
        )
    )


# ============================================================
# SOURCE-DIVERSE SELECTION
# ============================================================

def select_diverse_results(
    candidates: list[dict],
    n_results: int
) -> list[dict]:
    """
    Select final results while preserving relevance
    and encouraging source diversity.

    Strategy:

    1. Start from candidates already ranked by relevance.
    2. Prefer one result from each different source.
    3. If more results are still needed, fill the remaining
       slots using the original ranking.

    This helps multi-document questions avoid using all
    available context slots on a single document.
    """

    if n_results <= 0:
        return []

    if not candidates:
        return []

    selected = []
    selected_indexes = set()
    seen_sources = set()

    # --------------------------------------------------------
    # FIRST PASS: SOURCE DIVERSITY
    # --------------------------------------------------------

    for index, candidate in enumerate(
        candidates
    ):

        source = candidate.get(
            "source",
            "Unknown"
        )

        if source in seen_sources:
            continue

        selected.append(
            candidate
        )

        selected_indexes.add(
            index
        )

        seen_sources.add(
            source
        )

        if len(selected) >= n_results:
            return selected

    # --------------------------------------------------------
    # SECOND PASS: FILL REMAINING SLOTS
    # --------------------------------------------------------

    for index, candidate in enumerate(
        candidates
    ):

        if index in selected_indexes:
            continue

        selected.append(
            candidate
        )

        if len(selected) >= n_results:
            break

    return selected


# ============================================================
# SEMANTIC + LEXICAL SEARCH
# ============================================================

def search_documents(
    query: str,
    n_results: int = DEFAULT_N_RESULTS,
    max_distance: float = DEFAULT_MAX_DISTANCE
) -> list[dict]:
    """
    Search the vector database using hybrid retrieval.

    Steps:

    1. Generate a semantic embedding for the query.
    2. Retrieve a larger candidate set from ChromaDB.
    3. Remove candidates above the distance threshold.
    4. Calculate lexical relevance.
    5. Re-rank using lexical relevance and semantic distance.
    6. Select results while encouraging source diversity.
    """

    query_embedding = generate_embeddings(
        [query]
    )[0]

    vector_store = VectorStore()

    results = vector_store.search(
        query_embedding=query_embedding,
        n_results=max(
            n_results,
            CANDIDATE_RESULTS
        )
    )

    # --------------------------------------------------------
    # VALIDATE CHROMADB RESULTS
    # --------------------------------------------------------

    if not results.get(
        "documents"
    ):
        return []

    if not results["documents"][0]:
        return []

    documents = results[
        "documents"
    ][0]

    metadatas = results[
        "metadatas"
    ][0]

    distances = results[
        "distances"
    ][0]

    candidates = []

    # --------------------------------------------------------
    # FILTER + SCORE CANDIDATES
    # --------------------------------------------------------

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):

        if distance > max_distance:
            continue

        lexical = lexical_score(
            query,
            document
        )

        candidates.append(
            {
                "text": document,
                "page": metadata.get(
                    "page",
                    "Unknown"
                ),
                "source": metadata.get(
                    "source",
                    "Unknown"
                ),
                "distance": distance,
                "lexical_score": lexical,
            }
        )

    # --------------------------------------------------------
    # HYBRID RE-RANKING
    # --------------------------------------------------------

    candidates.sort(
        key=lambda item: (
            -item["lexical_score"],
            item["distance"],
        )
    )

    # --------------------------------------------------------
    # SOURCE-DIVERSE FINAL SELECTION
    # --------------------------------------------------------

    selected_candidates = (
        select_diverse_results(
            candidates=candidates,
            n_results=n_results,
        )
    )

    # --------------------------------------------------------
    # FINAL RESULTS
    # --------------------------------------------------------

    final_results = []

    for candidate in selected_candidates:

        final_results.append(
            {
                "text": candidate["text"],
                "page": candidate["page"],
                "source": candidate["source"],
                "distance": candidate["distance"],
            }
        )

    return final_results
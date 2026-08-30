from app.search import search_documents
from app.llm import generate_answer


# ============================================================
# CONFIGURATION
# ============================================================

DEFAULT_N_RESULTS = 2
MAX_CONTEXT_CHARS = 6000


# ============================================================
# CONTEXT BUILDER
# ============================================================

def build_context(
    results: list[dict],
    max_chars: int = MAX_CONTEXT_CHARS
) -> str:
    """
    Build the context passed to the LLM.

    Search results are already ordered by relevance.

    The total context size is limited to avoid sending
    unnecessarily large prompts to the local LLM.
    """

    context_parts = []
    current_length = 0

    for result in results:

        text = result["text"]
        source = result["source"]
        page = result["page"]

        chunk = (
            f"Source: {source}\n"
            f"Page: {page}\n\n"
            f"{text}\n"
        )

        # ----------------------------------------------------
        # Check context size
        # ----------------------------------------------------

        if current_length + len(chunk) > max_chars:

            remaining = max_chars - current_length

            # Add a partial chunk only if there is enough
            # room left to provide useful information.
            if remaining > 200:

                chunk = chunk[:remaining]

                context_parts.append(
                    chunk
                )

            break

        context_parts.append(
            chunk
        )

        current_length += len(chunk)

    return "\n\n".join(
        context_parts
    )


# ============================================================
# RAG PIPELINE
# ============================================================

def answer_question(
    question: str,
    n_results: int = DEFAULT_N_RESULTS
) -> dict:
    """
    Answer a question using the RAG pipeline.

    Steps:

    1. Retrieve relevant document chunks.
    2. Build a limited context.
    3. Send the context and question to the local LLM.
    4. Return the generated answer and its sources.
    """

    # --------------------------------------------------------
    # Retrieve documents
    # --------------------------------------------------------

    results = search_documents(
        question,
        n_results=n_results
    )

    # --------------------------------------------------------
    # No relevant information found
    # --------------------------------------------------------

    if not results:

        return {
            "answer": (
                "I don't have enough information in the "
                "provided document to answer this question."
            ),
            "sources": []
        }

    # --------------------------------------------------------
    # Build LLM context
    # --------------------------------------------------------

    context = build_context(
        results
    )

    # --------------------------------------------------------
    # Generate answer
    # --------------------------------------------------------

    answer = generate_answer(
        question=question,
        context=context
    )

    # --------------------------------------------------------
    # Return result
    # --------------------------------------------------------

    return {
        "answer": answer,
        "sources": results
    }
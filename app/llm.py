import time
import ollama


# ============================================================
# CONFIGURATION
# ============================================================

MODEL_NAME = "qwen2.5:3b"


# ============================================================
# GENERATE ANSWER
# ============================================================

def generate_answer(
    question: str,
    context: str
) -> str:
    """
    Generate an answer using the local Ollama LLM.

    The model is instructed to answer only from the
    retrieved document context.
    """

    # --------------------------------------------------------
    # Build prompt
    # --------------------------------------------------------

    prompt = f"""
You are an AI assistant that answers questions about documents.

Answer the user's question using ONLY the information contained
in the provided context.

If the context does not contain enough information to answer
the question, respond exactly with:

I don't have enough information in the provided document to answer this question.

Do not use outside knowledge.
Do not invent information.
Keep the answer concise and directly related to the question.

Context:
{context}

Question:
{question}

Answer:
""".strip()


    # --------------------------------------------------------
    # Measure Ollama request
    # --------------------------------------------------------

    start_time = time.time()

    response = ollama.generate(
        model=MODEL_NAME,
        prompt=prompt
    )

    total_time = time.time() - start_time


    # --------------------------------------------------------
    # Extract answer
    # --------------------------------------------------------

    answer = response.get(
        "response",
        ""
    ).strip()


    # --------------------------------------------------------
    # Performance information
    # --------------------------------------------------------

    prompt_eval_count = response.get(
        "prompt_eval_count",
        0
    )

    eval_count = response.get(
        "eval_count",
        0
    )

    load_duration = response.get(
        "load_duration",
        0
    ) / 1_000_000_000

    prompt_eval_duration = response.get(
        "prompt_eval_duration",
        0
    ) / 1_000_000_000

    eval_duration = response.get(
        "eval_duration",
        0
    ) / 1_000_000_000


    print("\n" + "=" * 60)
    print("OLLAMA PERFORMANCE")
    print("=" * 60)

    print(
        f"Model:                 {MODEL_NAME}"
    )

    print(
        f"Total Ollama time:     {total_time:.2f}s"
    )

    print(
        f"Model load time:       {load_duration:.2f}s"
    )

    print(
        f"Prompt evaluation:     {prompt_eval_duration:.2f}s"
    )

    print(
        f"Generation time:       {eval_duration:.2f}s"
    )

    print(
        f"Prompt tokens:         {prompt_eval_count}"
    )

    print(
        f"Generated tokens:      {eval_count}"
    )

    if eval_duration > 0:

        tokens_per_second = (
            eval_count / eval_duration
        )

        print(
            f"Generation speed:      "
            f"{tokens_per_second:.2f} tokens/s"
        )

    print("=" * 60)


    return answer
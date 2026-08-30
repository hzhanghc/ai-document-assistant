import time

from app.rag import answer_question


# ============================================================
# CONFIGURATION
# ============================================================

DOCUMENT_1 = "ai_document_assistant_benchmark.pdf"
DOCUMENT_2 = "ai_document_assistant_benchmark_2.pdf"

FALLBACK_ANSWER = (
    "I don't have enough information in the provided document "
    "to answer this question."
)


# ============================================================
# BENCHMARK TESTS
# ============================================================

TESTS = [

    # ========================================================
    # DOCUMENT 1 ONLY
    # ========================================================

    {
        "id": 1,
        "category": "Document 1",
        "question": (
            "How many document chunks per minute does "
            "the Aurora indexing service process?"
        ),
        "expected_sources": [DOCUMENT_1],
        "source_mode": "all",
        "expected_keywords": [
            "240",
        ],
        "relevant": True,
    },

    {
        "id": 2,
        "category": "Document 1",
        "question": (
            "How many candidate passages does the "
            "Borealis retrieval service return before re-ranking?"
        ),
        "expected_sources": [DOCUMENT_1],
        "source_mode": "all",
        "expected_keywords": [
            "Borealis",
            "7",
        ],
        "relevant": True,
    },

    {
        "id": 3,
        "category": "Document 1",
        "question": (
            "What is the code name of the benchmark "
            "deployment described in Volume 1?"
        ),
        "expected_sources": [DOCUMENT_1],
        "source_mode": "all",
        "expected_keywords": [
            "Cedar",
        ],
        "relevant": True,
    },

    {
        "id": 4,
        "category": "Document 1",
        "question": (
            "What is the cache expiration time for "
            "the Cedar metadata cache?"
        ),
        "expected_sources": [DOCUMENT_1],
        "source_mode": "all",
        "expected_keywords": [
            "45",
            "minute",
        ],
        "relevant": True,
    },

    {
        "id": 5,
        "category": "Document 1",
        "question": (
            "What are the three stages of the Cedar deployment "
            "in their exact order?"
        ),
        "expected_sources": [DOCUMENT_1],
        "source_mode": "all",
        "expected_keywords": [
            "ingestion",
            "retrieval",
            "generation",
        ],
        "relevant": True,
    },


    # ========================================================
    # DOCUMENT 2 ONLY
    # ========================================================

    {
        "id": 6,
        "category": "Document 2",
        "question": (
            "How many document chunks per minute does "
            "the Atlas ingestion service process?"
        ),
        "expected_sources": [DOCUMENT_2],
        "source_mode": "all",
        "expected_keywords": [
            "360",
        ],
        "relevant": True,
    },

    {
        "id": 7,
        "category": "Document 2",
        "question": (
            "How many candidate passages does the Meridian "
            "retrieval service return before re-ranking?"
        ),
        "expected_sources": [DOCUMENT_2],
        "source_mode": "all",
        "expected_keywords": [
            "Meridian",
            "9",
        ],
        "relevant": True,
    },

    {
        "id": 8,
        "category": "Document 2",
        "question": (
            "What is data leakage in machine learning?"
        ),
        "expected_sources": [DOCUMENT_2],
        "source_mode": "all",
        "expected_keywords": [
            "information",
            "training",
            "evaluation",
        ],
        "relevant": True,
    },

    {
        "id": 9,
        "category": "Document 2",
        "question": (
            "What is the difference between precision "
            "and recall?"
        ),
        "expected_sources": [DOCUMENT_2],
        "source_mode": "all",
        "expected_keywords": [
            "precision",
            "recall",
            "positive",
        ],
        "relevant": True,
    },

    {
        "id": 10,
        "category": "Document 2",
        "question": (
            "What is the cache expiration time for "
            "the Juniper metadata cache?"
        ),
        "expected_sources": [DOCUMENT_2],
        "source_mode": "all",
        "expected_keywords": [
            "30",
            "minute",
        ],
        "relevant": True,
    },


    # ========================================================
    # MULTI-DOCUMENT / COMPARISON
    # ========================================================

    {
        "id": 11,
        "category": "Multi-document",
        "question": (
            "Compare the processing rates of the "
            "Aurora and Atlas services."
        ),
        "expected_sources": [
            DOCUMENT_1,
            DOCUMENT_2,
        ],
        "source_mode": "all",
        "expected_keywords": [
            "Aurora",
            "240",
            "Atlas",
            "360",
        ],
        "relevant": True,
    },

    {
        "id": 12,
        "category": "Multi-document",
        "question": (
            "Compare the maximum candidate passage limits "
            "of Borealis and Meridian."
        ),
        "expected_sources": [
            DOCUMENT_1,
            DOCUMENT_2,
        ],
        "source_mode": "all",
        "expected_keywords": [
            "Borealis",
            "7",
            "Meridian",
            "9",
        ],
        "relevant": True,
    },

    {
        "id": 13,
        "category": "Multi-document",
        "question": (
            "Compare the metadata cache expiration times "
            "of Cedar and Juniper."
        ),
        "expected_sources": [
            DOCUMENT_1,
            DOCUMENT_2,
        ],
        "source_mode": "all",
        "expected_keywords": [
            "Cedar",
            "45",
            "Juniper",
            "30",
        ],
        "relevant": True,
    },

    {
        "id": 14,
        "category": "Multi-document",
        "question": (
            "What do the documents say about binary search "
            "and its time complexity?"
        ),
        "expected_sources": [
            DOCUMENT_1,
            DOCUMENT_2,
        ],
        "source_mode": "any",
        "expected_keywords": [
            "binary search",
            "log",
            "sorted",
        ],
        "relevant": True,
    },

    {
        "id": 15,
        "category": "Multi-document",
        "question": (
            "According to the documents, how does RAG use "
            "retrieval before generation?"
        ),
        "expected_sources": [
            DOCUMENT_1,
            DOCUMENT_2,
        ],
        "source_mode": "any",
        "expected_keywords": [
            "retriev",
            "context",
            "generation",
        ],
        "relevant": True,
    },


    # ========================================================
    # IRRELEVANT / OUT-OF-DOCUMENT
    # ========================================================

    {
        "id": 16,
        "category": "Irrelevant",
        "question": (
            "What is the capital of Ecuador?"
        ),
        "expected_sources": [],
        "source_mode": "none",
        "expected_keywords": [],
        "relevant": False,
    },

    {
        "id": 17,
        "category": "Irrelevant",
        "question": (
            "Who won the FIFA World Cup in 2022?"
        ),
        "expected_sources": [],
        "source_mode": "none",
        "expected_keywords": [],
        "relevant": False,
    },

    {
        "id": 18,
        "category": "Irrelevant",
        "question": (
            "What is the boiling point of water "
            "at sea level?"
        ),
        "expected_sources": [],
        "source_mode": "none",
        "expected_keywords": [],
        "relevant": False,
    },

    {
        "id": 19,
        "category": "Irrelevant",
        "question": (
            "Who wrote Don Quixote?"
        ),
        "expected_sources": [],
        "source_mode": "none",
        "expected_keywords": [],
        "relevant": False,
    },

    {
        "id": 20,
        "category": "Irrelevant",
        "question": (
            "What is the current weather in Tokyo?"
        ),
        "expected_sources": [],
        "source_mode": "none",
        "expected_keywords": [],
        "relevant": False,
    },
]


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def normalize_text(text: str) -> str:
    """
    Normalize text for simple answer validation.
    """

    return (
        text.lower()
        .replace("-", " ")
        .replace("_", " ")
        .strip()
    )


def get_retrieved_sources(result: dict) -> list[str]:
    """
    Return unique source document names from retrieved results.
    """

    sources = result.get(
        "sources",
        []
    )

    retrieved = []

    for source in sources:

        source_name = source.get(
            "source"
        )

        if (
            source_name
            and source_name not in retrieved
        ):
            retrieved.append(
                source_name
            )

    return retrieved


def check_retrieval(
    test: dict,
    result: dict
) -> bool:
    """
    Evaluate whether retrieval returned the expected
    document source or sources.
    """

    retrieved_sources = get_retrieved_sources(
        result
    )

    expected_sources = test[
        "expected_sources"
    ]

    mode = test[
        "source_mode"
    ]

    if mode == "none":

        answer = result.get(
            "answer",
            ""
        ).strip()

        return answer == FALLBACK_ANSWER

    if mode == "all":

        return all(
            source in retrieved_sources
            for source in expected_sources
        )

    if mode == "any":

        return any(
            source in retrieved_sources
            for source in expected_sources
        )

    return False


def check_answer(
    test: dict,
    result: dict
) -> bool:
    """
    Evaluate the generated answer.

    Relevant questions are checked using expected keywords.
    Irrelevant questions must return the exact fallback.
    """

    answer = result.get(
        "answer",
        ""
    ).strip()

    if not test["relevant"]:

        return answer == FALLBACK_ANSWER

    normalized_answer = normalize_text(
        answer
    )

    for keyword in test[
        "expected_keywords"
    ]:

        normalized_keyword = normalize_text(
            keyword
        )

        if normalized_keyword not in normalized_answer:
            return False

    return True


def format_sources(result: dict) -> str:
    """
    Create a readable representation of retrieved sources.
    """

    sources = result.get(
        "sources",
        []
    )

    if not sources:
        return "None"

    formatted = []

    for source in sources:

        document = source.get(
            "source",
            "Unknown"
        )

        page = source.get(
            "page",
            "Unknown"
        )

        distance = source.get(
            "distance"
        )

        if distance is not None:

            formatted.append(
                (
                    f"{document} "
                    f"(page {page}, "
                    f"distance {distance:.4f})"
                )
            )

        else:

            formatted.append(
                (
                    f"{document} "
                    f"(page {page})"
                )
            )

    return " | ".join(
        formatted
    )


# ============================================================
# BENCHMARK
# ============================================================

def run_benchmark() -> None:
    """
    Run the complete public RAG benchmark.
    """

    total_tests = len(
        TESTS
    )

    retrieval_passes = 0
    answer_passes = 0
    overall_passes = 0

    relevant_tests = 0
    irrelevant_tests = 0

    relevant_passes = 0
    irrelevant_passes = 0

    total_time = 0.0

    print(
        "\n"
        + "=" * 72
    )

    print(
        "AI DOCUMENT ASSISTANT - PUBLIC RAG BENCHMARK"
    )

    print(
        "=" * 72
    )

    print(
        f"Total tests: {total_tests}"
    )

    print(
        f"Document 1: {DOCUMENT_1}"
    )

    print(
        f"Document 2: {DOCUMENT_2}"
    )

    print(
        "=" * 72
    )

    for test in TESTS:

        print(
            "\n"
            + "-" * 72
        )

        print(
            (
                f"TEST {test['id']}/{total_tests} "
                f"[{test['category']}]"
            )
        )

        print(
            "-" * 72
        )

        print(
            f"Question: {test['question']}"
        )

        start_time = time.time()

        try:

            result = answer_question(
                test["question"]
            )

            elapsed = (
                time.time()
                - start_time
            )

            total_time += elapsed

            retrieval_ok = check_retrieval(
                test,
                result
            )

            answer_ok = check_answer(
                test,
                result
            )

            overall_ok = (
                retrieval_ok
                and answer_ok
            )

            if retrieval_ok:
                retrieval_passes += 1

            if answer_ok:
                answer_passes += 1

            if overall_ok:
                overall_passes += 1

            if test["relevant"]:

                relevant_tests += 1

                if overall_ok:
                    relevant_passes += 1

            else:

                irrelevant_tests += 1

                if overall_ok:
                    irrelevant_passes += 1

            answer = result.get(
                "answer",
                ""
            )

            print(
                "\nAnswer:"
            )

            print(
                answer
            )

            print(
                "\nSources:"
            )

            print(
                format_sources(
                    result
                )
            )

            print(
                "\nEvaluation:"
            )

            print(
                (
                    "Retrieval: "
                    f"{'PASS' if retrieval_ok else 'FAIL'}"
                )
            )

            print(
                (
                    "Answer:    "
                    f"{'PASS' if answer_ok else 'FAIL'}"
                )
            )

            print(
                (
                    "Overall:   "
                    f"{'PASS' if overall_ok else 'FAIL'}"
                )
            )

            print(
                f"Time:      {elapsed:.2f}s"
            )

        except Exception as error:

            elapsed = (
                time.time()
                - start_time
            )

            total_time += elapsed

            if test["relevant"]:
                relevant_tests += 1
            else:
                irrelevant_tests += 1

            print(
                "\nERROR:"
            )

            print(
                repr(error)
            )

            print(
                f"Time: {elapsed:.2f}s"
            )


    # ========================================================
    # FINAL SUMMARY
    # ========================================================

    retrieval_accuracy = (
        retrieval_passes
        / total_tests
        * 100
    )

    answer_accuracy = (
        answer_passes
        / total_tests
        * 100
    )

    overall_accuracy = (
        overall_passes
        / total_tests
        * 100
    )

    relevant_accuracy = (
        relevant_passes
        / relevant_tests
        * 100
        if relevant_tests
        else 0
    )

    irrelevant_accuracy = (
        irrelevant_passes
        / irrelevant_tests
        * 100
        if irrelevant_tests
        else 0
    )

    average_time = (
        total_time
        / total_tests
    )

    print(
        "\n\n"
        + "=" * 72
    )

    print(
        "BENCHMARK SUMMARY"
    )

    print(
        "=" * 72
    )

    print(
        (
            f"Retrieval accuracy: "
            f"{retrieval_passes}/{total_tests} "
            f"({retrieval_accuracy:.1f}%)"
        )
    )

    print(
        (
            f"Answer accuracy:    "
            f"{answer_passes}/{total_tests} "
            f"({answer_accuracy:.1f}%)"
        )
    )

    print(
        (
            f"Overall accuracy:   "
            f"{overall_passes}/{total_tests} "
            f"({overall_accuracy:.1f}%)"
        )
    )

    print()

    print(
        (
            f"Relevant questions: "
            f"{relevant_passes}/{relevant_tests} "
            f"({relevant_accuracy:.1f}%)"
        )
    )

    print(
        (
            f"Irrelevant questions: "
            f"{irrelevant_passes}/{irrelevant_tests} "
            f"({irrelevant_accuracy:.1f}%)"
        )
    )

    print()

    print(
        (
            f"Average response time: "
            f"{average_time:.2f}s"
        )
    )

    print(
        (
            f"Total benchmark time:  "
            f"{total_time:.2f}s"
        )
    )

    print(
        "=" * 72
    )


# ============================================================
# ENTRY POINT
# ============================================================

if __name__ == "__main__":
    run_benchmark()
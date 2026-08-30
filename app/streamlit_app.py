from pathlib import Path

import streamlit as st

from app.document_processor import (
    extract_text_from_pdf,
    create_chunks,
)
from app.embeddings import generate_embeddings
from app.rag import answer_question
from app.vector_store import VectorStore


# ============================================================
# CONFIGURATION
# ============================================================

APP_TITLE = "AI Document Assistant"

DATA_DIR = Path("data")
DOCUMENTS_DIR = DATA_DIR / "documents"

DOCUMENTS_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ============================================================
# STREAMLIT PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title=APP_TITLE,
    page_icon="📄",
    layout="wide",
)


# ============================================================
# SESSION STATE
# ============================================================

if "history" not in st.session_state:
    st.session_state.history = []

if "last_processed_document" not in st.session_state:
    st.session_state.last_processed_document = None


# ============================================================
# VECTOR STORE
# ============================================================

vector_store = VectorStore()


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def get_indexed_documents() -> dict[str, int]:
    """
    Return indexed document names and the number
    of chunks stored for each document.
    """

    stored_data = vector_store.get_documents()

    metadatas = stored_data.get(
        "metadatas",
        []
    )

    documents = {}

    for metadata in metadatas:

        if not metadata:
            continue

        source = metadata.get(
            "source",
            "Unknown"
        )

        documents[source] = (
            documents.get(source, 0) + 1
        )

    return documents


def save_uploaded_file(
    uploaded_file
) -> Path:
    """
    Save an uploaded PDF to the local documents directory.
    """

    destination = (
        DOCUMENTS_DIR
        / uploaded_file.name
    )

    with open(
        destination,
        "wb"
    ) as file:
        file.write(
            uploaded_file.getbuffer()
        )

    return destination


def process_document(
    uploaded_file
) -> dict:
    """
    Extract, chunk, embed, and index an uploaded PDF.
    """

    file_path = save_uploaded_file(
        uploaded_file
    )

    pages = extract_text_from_pdf(
        str(file_path)
    )

    if not pages:
        return {
            "success": False,
            "message": (
                "No extractable text was found "
                "in this PDF."
            ),
        }

    chunks = create_chunks(
        pages
    )

    if not chunks:
        return {
            "success": False,
            "message": (
                "The document did not produce "
                "any text chunks."
            ),
        }

    texts = [
        chunk["text"]
        for chunk in chunks
    ]

    embeddings = generate_embeddings(
        texts
    )

    source = uploaded_file.name

    # Remove previous chunks from this document
    # before re-indexing it.
    vector_store.delete_document(
        source
    )

    metadatas = []
    ids = []

    safe_source = (
        source
        .replace(" ", "_")
        .replace("/", "_")
        .replace("\\", "_")
    )

    for index, chunk in enumerate(chunks):

        metadatas.append(
            {
                "source": source,
                "page": chunk["page"],
            }
        )

        ids.append(
            (
                f"{safe_source}"
                f"_page_{chunk['page']}"
                f"_chunk_{index}"
            )
        )

    vector_store.add_documents(
        documents=texts,
        embeddings=embeddings,
        metadatas=metadatas,
        ids=ids,
    )

    return {
        "success": True,
        "pages": len(pages),
        "chunks": len(chunks),
        "embeddings": len(embeddings),
        "source": source,
    }


def display_sources(
    sources: list[dict]
) -> None:
    """
    Display source passages for the current answer.

    Expanders are used here, but this function is
    never called from inside another expander.
    """

    if not sources:
        st.caption(
            "No source passages were retrieved."
        )
        return

    for index, source in enumerate(
        sources,
        start=1
    ):

        source_name = source.get(
            "source",
            "Unknown"
        )

        page = source.get(
            "page",
            "Unknown"
        )

        text = source.get(
            "text",
            ""
        )

        distance = source.get(
            "distance"
        )

        label = (
            f"Source {index} — "
            f"{source_name}, "
            f"page {page}"
        )

        with st.expander(
            label
        ):

            if distance is not None:
                st.caption(
                    (
                        "Semantic distance: "
                        f"{distance:.4f}"
                    )
                )

            if text:
                st.write(
                    text
                )
            else:
                st.write(
                    "No source text available."
                )


def display_history_item(
    result: dict
) -> None:
    """
    Display a previous question and answer safely.

    No nested expanders are used here.
    """

    question = result.get(
        "question"
    )

    answer = result.get(
        "answer",
        (
            "No answer is available "
            "for this history entry."
        )
    )

    sources = result.get(
        "sources",
        []
    )

    if question:
        st.markdown(
            f"### {question}"
        )
    else:
        st.markdown(
            "### Previous question"
        )

    st.write(
        answer
    )

    if sources:

        st.markdown(
            "**Sources**"
        )

        for index, source in enumerate(
            sources,
            start=1
        ):

            source_name = source.get(
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

                st.caption(
                    (
                        f"Source {index}: "
                        f"{source_name} — "
                        f"Page {page} — "
                        f"Distance {distance:.4f}"
                    )
                )

            else:

                st.caption(
                    (
                        f"Source {index}: "
                        f"{source_name} — "
                        f"Page {page}"
                    )
                )


# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.header(
        "Knowledge Base"
    )

    total_chunks = vector_store.count()

    st.metric(
        "Total chunks",
        total_chunks
    )

    indexed_documents = (
        get_indexed_documents()
    )

    st.subheader(
        "Indexed documents"
    )

    if indexed_documents:

        for document_name, chunk_count in (
            indexed_documents.items()
        ):

            st.write(
                f"📄 {document_name}"
            )

            st.caption(
                f"{chunk_count} chunks"
            )

    else:

        st.info(
            "No documents are currently indexed."
        )

    st.divider()

    if st.button(
        "Clear knowledge base",
        use_container_width=True,
    ):

        vector_store.reset()

        st.session_state.history = []

        st.session_state[
            "last_processed_document"
        ] = None

        st.success(
            "Knowledge base cleared."
        )

        st.rerun()


# ============================================================
# MAIN HEADER
# ============================================================

st.title(
    "📄 AI Document Assistant"
)

st.write(
    (
        "Upload PDF documents, index their contents, "
        "and ask questions using a local RAG pipeline."
    )
)


# ============================================================
# DOCUMENT UPLOAD
# ============================================================

st.header(
    "1. Add a document"
)

uploaded_file = st.file_uploader(
    "Upload a PDF",
    type=["pdf"],
)


if uploaded_file is not None:

    st.write(
        (
            "Selected file: "
            f"**{uploaded_file.name}**"
        )
    )

    if st.button(
        "Process document",
        type="primary",
    ):

        with st.spinner(
            "Processing and indexing document..."
        ):

            try:

                processing_result = (
                    process_document(
                        uploaded_file
                    )
                )

                if not processing_result.get(
                    "success",
                    False
                ):

                    st.error(
                        processing_result.get(
                            "message",
                            (
                                "The document could "
                                "not be processed."
                            )
                        )
                    )

                else:

                    st.session_state[
                        "last_processed_document"
                    ] = uploaded_file.name

                    st.success(
                        "Document indexed successfully."
                    )

                    column_1, column_2, column_3 = (
                        st.columns(3)
                    )

                    column_1.metric(
                        "Pages extracted",
                        processing_result.get(
                            "pages",
                            0
                        )
                    )

                    column_2.metric(
                        "Chunks created",
                        processing_result.get(
                            "chunks",
                            0
                        )
                    )

                    column_3.metric(
                        "Embeddings generated",
                        processing_result.get(
                            "embeddings",
                            0
                        )
                    )

            except Exception as error:

                st.error(
                    (
                        "An error occurred while "
                        "processing the document."
                    )
                )

                st.exception(
                    error
                )


# ============================================================
# QUESTION ANSWERING
# ============================================================

st.divider()

st.header(
    "2. Ask a question"
)


if vector_store.count() == 0:

    st.info(
        (
            "Add at least one PDF to the knowledge base "
            "before asking questions."
        )
    )

else:

    question = st.text_input(
        "Question",
        placeholder=(
            "Ask something about your "
            "indexed documents..."
        ),
    )

    ask_button = st.button(
        "Ask",
        type="primary",
    )

    if ask_button:

        clean_question = (
            question.strip()
            if question
            else ""
        )

        if not clean_question:

            st.warning(
                "Enter a question first."
            )

        else:

            with st.spinner(
                (
                    "Searching documents and "
                    "generating answer..."
                )
            ):

                try:

                    rag_result = answer_question(
                        clean_question
                    )

                    history_result = {
                        "question": clean_question,
                        "answer": rag_result.get(
                            "answer",
                            "No answer was generated."
                        ),
                        "sources": rag_result.get(
                            "sources",
                            []
                        ),
                    }

                    st.session_state.history.append(
                        history_result
                    )

                    st.success(
                        "Answer generated."
                    )

                    st.markdown(
                        "### Answer"
                    )

                    st.write(
                        history_result[
                            "answer"
                        ]
                    )

                    if history_result[
                        "sources"
                    ]:

                        st.markdown(
                            "### Sources"
                        )

                        display_sources(
                            history_result[
                                "sources"
                            ]
                        )

                except Exception as error:

                    st.error(
                        (
                            "An error occurred while "
                            "answering the question."
                        )
                    )

                    st.exception(
                        error
                    )


# ============================================================
# QUESTION HISTORY
# ============================================================

st.divider()

st.header(
    "Question History"
)


history = st.session_state.get(
    "history",
    []
)


if not history:

    st.caption(
        (
            "No questions have been asked "
            "during this session yet."
        )
    )

else:

    valid_history = [
        item
        for item in history
        if isinstance(
            item,
            dict
        )
    ]

    for index, result in enumerate(
        reversed(
            valid_history
        )
    ):

        display_history_item(
            result
        )

        if index < len(
            valid_history
        ) - 1:

            st.divider()
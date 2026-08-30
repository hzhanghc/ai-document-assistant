import pymupdf


def extract_text_from_pdf(file_path: str) -> list[dict]:
    """
    Extract text from a PDF while preserving page information.

    Returns:
        A list containing the text and page number for each page.
    """

    document = pymupdf.open(file_path)

    pages = []

    for page_number, page in enumerate(document, start=1):
        text = page.get_text("text").strip()

        if text:
            pages.append({
                "page": page_number,
                "text": text
            })

    document.close()

    return pages


def create_chunks(
    pages: list[dict],
    chunk_size: int = 500,
    overlap: int = 100
) -> list[dict]:
    """
    Split extracted text into overlapping chunks.

    Args:
        pages: List of pages containing text and page numbers.
        chunk_size: Approximate number of words per chunk.
        overlap: Number of words shared between consecutive chunks.

    Returns:
        List of chunks containing text and source page.
    """

    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    chunks = []

    for page in pages:
        words = page["text"].split()

        start = 0

        while start < len(words):
            end = start + chunk_size

            chunk_words = words[start:end]

            if chunk_words:
                chunks.append({
                    "text": " ".join(chunk_words),
                    "page": page["page"]
                })

            if end >= len(words):
                break

            start = end - overlap

    return chunks
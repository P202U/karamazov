import fitz


def parse_pdf(file_bytes: bytes) -> str:
    """Extracts text from a PDF byte stream safely."""
    text_parts = []
    try:
        with fitz.open(stream=file_bytes, filetype="pdf") as doc:
            for page in doc:
                content = page.get_text("text")
                if isinstance(content, str):
                    text_parts.append(content)

        return "\n".join(text_parts).strip()
    except Exception as e:
        raise ValueError(f"Could not parse PDF: {e}") from e

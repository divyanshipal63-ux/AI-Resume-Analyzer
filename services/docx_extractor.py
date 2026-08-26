from docx import Document


def extract_docx_text(file_path):
    """
    Extract text from a DOCX resume.

    Args:
        file_path: Path to the DOCX resume.

    Returns:
        Extracted text as a string.
    """

    text = ""

    try:
        document = Document(file_path)

        for paragraph in document.paragraphs:
            text += paragraph.text + "\n"

        return text.strip()

    except Exception as e:
        raise Exception(f"Error extracting DOCX text: {e}")

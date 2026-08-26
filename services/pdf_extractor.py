import fitz


def extract_pdf_text(file_path):
    """
    Extract text from a PDF file.

    Args:
        file_path: Path to the PDF resume.

    Returns:
        Extracted text as a string.
    """

    text = ""

    try:
        pdf = fitz.open(file_path)

        for page in pdf:
            text += page.get_text()

        pdf.close()

        return text.strip()

    except Exception as e:
        raise Exception(f"Error extracting PDF text: {e}")

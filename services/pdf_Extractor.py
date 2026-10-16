
import pymupdf


def extract_text_from_pdf(file_path):
    """
    Extract text from a PDF resume.

    Args:
        file_path: Path to the PDF file.

    Returns:
        Extracted text as a string.
    """
    try:
        with pymupdf.open(file_path) as pdf:
            pages_text = []

            for page in pdf:
                text = page.get_text()
                if text:
                    pages_text.append(text)

            extracted_text = "\n".join(pages_text).strip()

            if not extracted_text:
                raise ValueError(
                    "No readable text found in the PDF. "
                    "It may be a scanned document."
                )

            return extracted_text

    except (pymupdf.FileDataError, ValueError):
        raise
    except Exception as error:
        raise RuntimeError(
            f"Failed to extract text from PDF: {error}"
        ) from error

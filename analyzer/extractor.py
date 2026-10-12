"""
Resume Text Extractor module.
Supports PDF (pdfplumber with pdfminer fallback) and DOCX (python-docx).
Handles in-memory parsing to guarantee total user privacy.
"""
import io
import re
from typing import Dict, Any, Tuple


def clean_extracted_text(text: str) -> str:
    """Normalize extracted text whitespace and line breaks."""
    if not text:
        return ""
    # Replace non-breaking spaces and weird unicode whitespace
    text = text.replace('\xa0', ' ').replace('\u200b', '')
    # Replace multiple spaces with single space, preserve paragraphs
    text = re.sub(r'[ \t]+', ' ', text)
    # Collapse 3+ newlines into 2
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def extract_from_pdf(file_bytes: bytes) -> Tuple[str, Dict[str, Any]]:
    """
    Extract text and metadata from PDF bytes using pdfplumber.
    Falls back gracefully if issues occur.
    """
    metadata = {
        "pages": 0,
        "char_count": 0,
        "word_count": 0,
        "has_images_or_tables": False,
        "parser": "pdfplumber"
    }
    extracted_pages = []

    try:
        import pdfplumber
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            metadata["pages"] = len(pdf.pages)
            for page_num, page in enumerate(pdf.pages, start=1):
                page_text = page.extract_text(layout=True) or page.extract_text() or ""
                if page_text.strip():
                    extracted_pages.append(page_text.strip())
                # Check for tables
                if page.extract_tables():
                    metadata["has_images_or_tables"] = True

    except Exception as e:
        # Fallback to pdfminer if pdfplumber encounters an edge case
        try:
            from pdfminer.high_level import extract_text as pdfminer_extract
            fallback_text = pdfminer_extract(io.BytesIO(file_bytes))
            if fallback_text and fallback_text.strip():
                extracted_pages = [fallback_text.strip()]
                metadata["parser"] = "pdfminer.six (fallback)"
        except Exception as e2:
            raise ValueError(f"Unable to read PDF file. It might be password-protected or corrupted. Error: {str(e)}")

    full_text = "\n\n".join(extracted_pages)
    cleaned = clean_extracted_text(full_text)

    if not cleaned:
        raise ValueError(
            "No readable text could be extracted from this PDF. "
            "It may be a scanned image or photograph. Please use a text-based PDF or paste your resume text directly."
        )

    metadata["char_count"] = len(cleaned)
    metadata["word_count"] = len(cleaned.split())
    return cleaned, metadata


def extract_from_docx(file_bytes: bytes) -> Tuple[str, Dict[str, Any]]:
    """
    Extract text from DOCX bytes using python-docx.
    Extracts paragraphs, table cells, and headers.
    """
    metadata = {
        "paragraphs": 0,
        "char_count": 0,
        "word_count": 0,
        "has_tables": False,
        "parser": "python-docx"
    }

    try:
        import docx
        doc = docx.Document(io.BytesIO(file_bytes))
        paragraphs = []

        for p in doc.paragraphs:
            if p.text.strip():
                paragraphs.append(p.text.strip())

        # Extract table content if present
        if doc.tables:
            metadata["has_tables"] = True
            for table in doc.tables:
                for row in table.rows:
                    row_texts = [cell.text.strip() for cell in row.cells if cell.text.strip()]
                    if row_texts:
                        # De-duplicate adjacent identical cells (merged cells)
                        unique_cells = []
                        for cell_text in row_texts:
                            if not unique_cells or cell_text != unique_cells[-1]:
                                unique_cells.append(cell_text)
                        paragraphs.append(" | ".join(unique_cells))

        full_text = "\n".join(paragraphs)
        cleaned = clean_extracted_text(full_text)

        if not cleaned:
            raise ValueError("The uploaded DOCX file appears to be empty or contains only non-text media.")

        metadata["paragraphs"] = len(paragraphs)
        metadata["char_count"] = len(cleaned)
        metadata["word_count"] = len(cleaned.split())
        return cleaned, metadata

    except Exception as e:
        if "ValueError" in type(e).__name__:
            raise
        raise ValueError(f"Unable to parse DOCX document. Ensure it is a valid .docx file: {str(e)}")


def extract_resume_text(filename: str, file_bytes: bytes) -> Tuple[str, Dict[str, Any]]:
    """
    Dispatcher to extract text based on file extension.
    """
    fn_lower = filename.lower()
    if fn_lower.endswith('.pdf'):
        return extract_from_pdf(file_bytes)
    elif fn_lower.endswith('.docx'):
        return extract_from_docx(file_bytes)
    elif fn_lower.endswith('.txt'):
        text = file_bytes.decode('utf-8', errors='ignore')
        cleaned = clean_extracted_text(text)
        if not cleaned:
            raise ValueError("The uploaded text file is empty.")
        return cleaned, {
            "parser": "plain-text",
            "word_count": len(cleaned.split()),
            "char_count": len(cleaned)
        }
    else:
        raise ValueError("Unsupported file format. Please upload a PDF (.pdf), Word document (.docx), or plain text (.txt).")

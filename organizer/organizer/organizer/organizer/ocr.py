try:
    import pytesseract
    from PIL import Image
except ImportError:  # pragma: no cover
    pytesseract = None
    Image = None


def ocr_image(path: str) -> str:
    """Return OCR text for a local image file (requires `pytesseract`)."""
    if pytesseract is None:
        raise RuntimeError("pytesseract not installed. Install with 'pip install onedrive-organizer[ocr]'")
    return pytesseract.image_to_string(Image.open(path))

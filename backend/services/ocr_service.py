import base64
from pathlib import Path


class OCRService:
    """Modular OCR placeholder. Replace internals with Tesseract or a cloud OCR later."""

    def extract_text(self, file_path: str, content_type: str) -> str:
        path = Path(file_path)
        if content_type == "application/pdf":
            return (
                "OCR placeholder: PDF text extraction is not enabled yet. "
                f"File '{path.name}' received. Integrate Tesseract, PyMuPDF, or OCR API here."
            )

        raw_bytes = path.read_bytes()
        preview = base64.b64encode(raw_bytes[:96]).decode("utf-8")
        return (
            "OCR placeholder: Image text extraction is not enabled yet. "
            f"File '{path.name}' received. Base64 preview: {preview}. "
            "Replace this service with Tesseract or another OCR engine."
        )

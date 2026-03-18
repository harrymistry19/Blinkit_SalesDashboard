import os
from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from utils.config import settings
from utils.constants import ALLOWED_CONTENT_TYPES

router = APIRouter(prefix="/upload", tags=["upload"])
UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("")
async def upload_invoice(file: UploadFile = File(...)) -> dict[str, str | int]:
    if file.content_type not in ALLOWED_CONTENT_TYPES:
        raise HTTPException(status_code=400, detail="Only invoice PDF, JPG, and PNG files are supported.")

    content = await file.read()
    max_bytes = settings.max_upload_mb * 1024 * 1024
    if len(content) > max_bytes:
        raise HTTPException(status_code=400, detail=f"File exceeds {settings.max_upload_mb} MB limit.")

    filename = f"{uuid4()}-{file.filename}"
    destination = UPLOAD_DIR / filename
    destination.write_bytes(content)

    return {
        "filename": file.filename,
        "stored_name": filename,
        "content_type": file.content_type or "application/octet-stream",
        "size": len(content),
        "path": os.fspath(destination),
    }

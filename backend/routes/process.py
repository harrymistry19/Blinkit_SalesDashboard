from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from models.database import get_db
from models.history import InvoiceHistory
from models.schemas import InvoiceOutput, ProcessResponse
from services.ai_processor import AIProcessor
from services.invoice_parser import InvoiceParser
from services.ocr_service import OCRService

router = APIRouter(prefix="/process", tags=["process"])
ocr_service = OCRService()
ai_processor = AIProcessor()
invoice_parser = InvoiceParser()


class ProcessRequest(BaseModel):
    path: str
    filename: str
    content_type: str


@router.post("", response_model=ProcessResponse)
async def process_invoice(request: ProcessRequest, db: Session = Depends(get_db)):
    if "invoice" not in request.filename.lower() and request.content_type == "application/octet-stream":
        raise HTTPException(status_code=400, detail="Only invoice files are supported.")

    raw_text = ocr_service.extract_text(request.path, request.content_type)
    extracted = await ai_processor.process_invoice_text(raw_text)
    warnings, confidence_scores, field_sources = invoice_parser.validate(extracted, raw_text)
    extracted["warnings"] = warnings
    extracted["confidence_scores"] = confidence_scores
    extracted["raw_text_preview"] = raw_text[:1500]
    extracted["field_sources"] = field_sources

    record = InvoiceHistory(
        filename=request.filename,
        content_type=request.content_type,
        raw_text=raw_text,
        extracted_data=extracted,
        warnings=warnings,
    )
    db.add(record)
    db.commit()
    db.refresh(record)

    return ProcessResponse(
        id=record.id,
        filename=record.filename,
        content_type=record.content_type,
        extracted_data=InvoiceOutput.model_validate(record.extracted_data),
        created_at=record.created_at,
    )

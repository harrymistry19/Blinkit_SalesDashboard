from fastapi import APIRouter, Depends
from sqlalchemy import desc
from sqlalchemy.orm import Session

from models.database import get_db
from models.history import InvoiceHistory
from models.schemas import HistoryResponse

router = APIRouter(prefix="/history", tags=["history"])


@router.get("", response_model=list[HistoryResponse])
def fetch_history(db: Session = Depends(get_db)):
    records = db.query(InvoiceHistory).order_by(desc(InvoiceHistory.created_at)).all()
    return [
        HistoryResponse(
            id=record.id,
            filename=record.filename,
            content_type=record.content_type,
            extracted_data=record.extracted_data,
            warnings=record.warnings,
            created_at=record.created_at,
        )
        for record in records
    ]

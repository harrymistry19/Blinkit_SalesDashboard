from datetime import datetime

from sqlalchemy import DateTime, Integer, JSON, String
from sqlalchemy.orm import Mapped, mapped_column

from models.database import Base


class InvoiceHistory(Base):
    __tablename__ = "invoice_history"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    filename: Mapped[str] = mapped_column(String(255), nullable=False)
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)
    raw_text: Mapped[str] = mapped_column(String, nullable=False)
    extracted_data: Mapped[dict] = mapped_column(JSON, nullable=False)
    warnings: Mapped[list] = mapped_column(JSON, nullable=False, default=list)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)

from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field


class CompanyDetails(BaseModel):
    name: str | None = None
    address: str | None = None
    gstin: str | None = None
    contact: str | None = None


class InvoiceDetails(BaseModel):
    invoice_number: str | None = None
    invoice_date: str | None = None
    due_date: str | None = None


class CustomerDetails(BaseModel):
    name: str | None = None
    address: str | None = None
    gstin: str | None = None


class InvoiceItem(BaseModel):
    description: str | None = None
    quantity: str | None = None
    rate: str | None = None
    amount: str | None = None
    confidence: float | None = None


class TaxDetails(BaseModel):
    cgst: str | None = None
    sgst: str | None = None
    igst: str | None = None


class PaymentDetails(BaseModel):
    bank_name: str | None = None
    account_number: str | None = None
    ifsc: str | None = None


class InvoiceOutput(BaseModel):
    company_details: CompanyDetails = Field(default_factory=CompanyDetails)
    invoice_details: InvoiceDetails = Field(default_factory=InvoiceDetails)
    customer_details: CustomerDetails = Field(default_factory=CustomerDetails)
    items: list[InvoiceItem] = Field(default_factory=list)
    tax_details: TaxDetails = Field(default_factory=TaxDetails)
    total_amount: str | None = None
    payment_details: PaymentDetails = Field(default_factory=PaymentDetails)
    confidence_scores: dict[str, float | None] = Field(default_factory=dict)
    warnings: list[str] = Field(default_factory=list)
    raw_text_preview: str | None = None
    field_sources: dict[str, str] = Field(default_factory=dict)


class ProcessResponse(BaseModel):
    id: int
    filename: str
    content_type: str
    extracted_data: InvoiceOutput
    created_at: datetime


class HistoryResponse(BaseModel):
    id: int
    filename: str
    content_type: str
    extracted_data: dict[str, Any]
    warnings: list[str]
    created_at: datetime

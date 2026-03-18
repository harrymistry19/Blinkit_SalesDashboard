ALLOWED_CONTENT_TYPES = {
    "application/pdf",
    "image/jpeg",
    "image/png",
}

STRICT_GROQ_SYSTEM_PROMPT = (
    "You are an expert invoice parser. You ONLY extract data from invoices. "
    "Do NOT answer anything outside invoice context. Return STRICT JSON only. "
    "Do NOT add explanations. Do NOT hallucinate. If value not found → return null."
)

STRICT_OUTPUT_TEMPLATE = {
    "company_details": {
        "name": None,
        "address": None,
        "gstin": None,
        "contact": None,
    },
    "invoice_details": {
        "invoice_number": None,
        "invoice_date": None,
        "due_date": None,
    },
    "customer_details": {
        "name": None,
        "address": None,
        "gstin": None,
    },
    "items": [
        {
            "description": None,
            "quantity": None,
            "rate": None,
            "amount": None,
        }
    ],
    "tax_details": {
        "cgst": None,
        "sgst": None,
        "igst": None,
    },
    "total_amount": None,
    "payment_details": {
        "bank_name": None,
        "account_number": None,
        "ifsc": None,
    },
}

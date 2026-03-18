import json
from typing import Any

import httpx

from services.invoice_parser import InvoiceParser
from utils.config import settings
from utils.constants import STRICT_GROQ_SYSTEM_PROMPT


class AIProcessor:
    def __init__(self) -> None:
        self.parser = InvoiceParser()

    async def process_invoice_text(self, raw_text: str) -> dict[str, Any]:
        if not settings.groq_api_key:
            return self.parser.normalize_output(None)

        prompt = (
            "Extract invoice data from the following OCR text. "
            "Return strict JSON matching the required invoice schema and use null for missing values.\n\n"
            f"OCR TEXT:\n{raw_text}"
        )

        payload = {
            "model": settings.groq_model,
            "temperature": 0,
            "response_format": {"type": "json_object"},
            "messages": [
                {"role": "system", "content": STRICT_GROQ_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        }

        async with httpx.AsyncClient(timeout=60) as client:
            response = await client.post(
                "https://api.groq.com/openai/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {settings.groq_api_key}",
                    "Content-Type": "application/json",
                },
                json=payload,
            )
            response.raise_for_status()
            data = response.json()

        content = data["choices"][0]["message"]["content"]
        normalized = self.parser.normalize_output(content)
        if not isinstance(normalized, dict):
            return self.parser.normalize_output(None)
        return normalized

    def sample_groq_request(self, raw_text: str) -> dict[str, Any]:
        return {
            "model": settings.groq_model,
            "messages": [
                {"role": "system", "content": STRICT_GROQ_SYSTEM_PROMPT},
                {
                    "role": "user",
                    "content": (
                        "Extract invoice data only and respond with strict JSON.\n\n"
                        f"OCR TEXT:\n{raw_text}"
                    ),
                },
            ],
            "temperature": 0,
            "response_format": {"type": "json_object"},
        }

import copy
import json
import re
from decimal import Decimal, InvalidOperation
from typing import Any

from utils.constants import STRICT_OUTPUT_TEMPLATE


def _safe_decimal(value: str | None) -> Decimal | None:
    if value in (None, ""):
        return None
    cleaned = re.sub(r"[^\d.-]", "", value)
    if not cleaned:
        return None
    try:
        return Decimal(cleaned)
    except InvalidOperation:
        return None


class InvoiceParser:
    def normalize_output(self, payload: dict[str, Any] | str | None) -> dict[str, Any]:
        base = copy.deepcopy(STRICT_OUTPUT_TEMPLATE)
        if payload is None:
            return base
        if isinstance(payload, str):
            payload = self._parse_json_string(payload)
        if not isinstance(payload, dict):
            return base
        return self._deep_merge(base, payload)

    def _parse_json_string(self, raw: str) -> dict[str, Any] | None:
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", raw, flags=re.DOTALL)
            if not match:
                return None
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                return None

    def _deep_merge(self, base: Any, incoming: Any) -> Any:
        if isinstance(base, dict) and isinstance(incoming, dict):
            merged = {}
            for key, value in base.items():
                merged[key] = self._deep_merge(value, incoming.get(key))
            for key, value in incoming.items():
                if key not in merged:
                    merged[key] = value
            return merged
        if isinstance(base, list):
            if isinstance(incoming, list):
                return incoming
            return [] if incoming == [] else base
        return incoming if incoming is not None else None

    def validate(self, invoice_data: dict[str, Any], raw_text: str) -> tuple[list[str], dict[str, float | None], dict[str, str]]:
        warnings: list[str] = []
        confidence_scores: dict[str, float | None] = {}
        field_sources: dict[str, str] = {}

        invoice_number = invoice_data["invoice_details"].get("invoice_number")
        if not invoice_number:
            warnings.append("Invoice number missing.")

        total_amount = _safe_decimal(invoice_data.get("total_amount"))
        item_total = sum((_safe_decimal(item.get("amount")) or Decimal("0")) for item in invoice_data.get("items", []))
        tax_total = sum(
            (_safe_decimal(invoice_data.get("tax_details", {}).get(field)) or Decimal("0"))
            for field in ("cgst", "sgst", "igst")
        )
        if total_amount is not None and (item_total or tax_total):
            expected_total = item_total + tax_total
            if abs(expected_total - total_amount) > Decimal("1.00"):
                warnings.append(
                    f"Total mismatch detected. Expected {expected_total} from items + tax, found {total_amount}."
                )

        if not invoice_data.get("company_details", {}).get("gstin") and re.search(r"\bGST\b|\bGSTIN\b", raw_text, re.I):
            warnings.append("GST mentioned in document text but structured GSTIN could not be extracted.")

        def traverse(prefix: str, value: Any):
            if isinstance(value, dict):
                for k, v in value.items():
                    traverse(f"{prefix}.{k}" if prefix else k, v)
            elif isinstance(value, list):
                for index, item in enumerate(value):
                    traverse(f"{prefix}[{index}]", item)
            else:
                if value is None or value == "":
                    confidence_scores[prefix] = None
                else:
                    confidence_scores[prefix] = 0.92 if str(value).lower() in raw_text.lower() else 0.7
                    field_sources[prefix] = self._match_source(str(value), raw_text)

        traverse("", invoice_data)
        return warnings, confidence_scores, field_sources

    def _match_source(self, value: str, raw_text: str) -> str:
        pattern = re.escape(value.strip())
        match = re.search(pattern, raw_text, re.IGNORECASE)
        if not match:
            return ""
        start = max(0, match.start() - 40)
        end = min(len(raw_text), match.end() + 40)
        return raw_text[start:end].replace("\n", " ").strip()

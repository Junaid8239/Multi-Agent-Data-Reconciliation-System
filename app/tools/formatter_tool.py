import json
from crewai.tools import BaseTool

class FormatterTool(BaseTool):
    name: str = "format_final_record"
    description: str = (
        "Takes extracted fields and DB validation result (JSON strings) "
        "and merges them into the final standardized record schema. "
        "This tool's output is authoritative — do not alter the values it returns."
    )

    def _run(self, extracted_json: str, validation_json: str) -> str:
        extracted = json.loads(extracted_json)
        validation = json.loads(validation_json)
        matched = validation.get("match", False)

        final = {
            "input_name": extracted.get("name"),
            "input_email": extracted.get("email"),
            "input_phone": extracted.get("phone"),
            "matched_in_db": matched,
            "customer_id": validation.get("customer_id") if matched else None,
            "canonical_name": validation.get("full_name") if matched else None,
            "canonical_email": validation.get("email") if matched else None,
            "canonical_phone": validation.get("phone") if matched else None,
            "canonical_address": validation.get("address") if matched else None,
            "match_confidence": validation.get("match_score", 0) if matched else 0,
        }
        return json.dumps(final)
import json
from crewai.tools import BaseTool

class FormatterTool(BaseTool):
    name: str = "format_final_record"
    description: str = (
        "Takes extracted fields and DB validation result (JSON strings) "
        "and merges them into the final standardized record schema."
    )

    def _run(self, extracted_json: str, validation_json: str) -> str:
        extracted = json.loads(extracted_json)
        matched = validation_json != "NO_MATCH"
        validation = json.loads(validation_json) if matched else {}

        final = {
            "input_name": extracted.get("name"),
            "input_email": extracted.get("email"),
            "input_phone": extracted.get("phone"),
            "matched_in_db": matched,
            "customer_id": validation.get("customer_id"),
            "canonical_name": validation.get("full_name"),
            "canonical_email": validation.get("email"),
            "canonical_phone": validation.get("phone"),
            "canonical_address": validation.get("address"),
            "match_confidence": validation.get("match_score", 0),
        }
        return json.dumps(final)
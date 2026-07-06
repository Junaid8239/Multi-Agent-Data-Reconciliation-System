import re
import json
from crewai.tools import BaseTool

class ExtractionTool(BaseTool):
    name: str = "extract_record_fields"
    description: str = (
        "Takes a raw, messy text record and extracts structured fields: "
        "name, email, phone, address. Input is a raw string. "
        "Returns a JSON string of the extracted fields."
    )

    def _run(self, raw_text: str) -> str:
        email_match = re.search(r"[\w\.-]+@[\w\.-]+\.\w+", raw_text)
        phone_match = re.search(r"(\+?\d[\d\-\s\(\)]{7,}\d)", raw_text)

        # crude name heuristic: text before first comma or email
        name_part = raw_text.split(",")[0].strip()
        name_part = re.sub(r"\s+", " ", name_part)

        extracted = {
            "name": name_part or None,
            "email": email_match.group(0) if email_match else None,
            "phone": phone_match.group(0).strip() if phone_match else None,
            "raw_address_guess": raw_text,
        }
        return json.dumps(extracted)

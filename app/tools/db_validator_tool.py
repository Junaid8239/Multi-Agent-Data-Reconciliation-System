import json
from thefuzz import fuzz
from crewai.tools import BaseTool
from sqlalchemy import text
from app.db.session import engine

class DBValidatorTool(BaseTool):
    name: str = "validate_against_database"
    description: str = (
        "Takes a JSON string of extracted fields (name, email, phone) and "
        "checks them against the customers table in SQL Server. "
        "Returns the best-matching DB record with a similarity score, "
        "or 'NO_MATCH' if nothing scores above threshold."
    )

    def _run(self, extracted_json: str) -> str:
        data = json.loads(extracted_json)
        name = (data.get("name") or "").lower()
        email = (data.get("email") or "").lower()

        with engine.connect() as conn:
            rows = conn.execute(text(
                "SELECT customer_id, full_name, email, phone, address FROM customers"
            )).mappings().all()

        best_score, best_row = 0, None
        for row in rows:
            score = fuzz.token_sort_ratio(name, row["full_name"].lower())
            if email and email == row["email"].lower():
                score = 100  # exact email match wins
            if score > best_score:
                best_score, best_row = score, row

        if best_row and best_score >= 75:
            result = dict(best_row)
            result["match_score"] = best_score
            return json.dumps(result, default=str)

        return "NO_MATCH"
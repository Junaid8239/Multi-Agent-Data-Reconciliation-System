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
        "Returns a JSON string: {\"match\": true, ...fields, \"match_score\": N} "
        "if a confident match is found, or {\"match\": false} if not."
    )

    def _run(self, extracted_json: str) -> str:
        data = json.loads(extracted_json)
        name = (data.get("name") or "").lower().strip()
        email = (data.get("email") or "").lower().strip()

        if not name and not email:
            return json.dumps({"match": False})

        with engine.connect() as conn:
            rows = conn.execute(text(
                "SELECT customer_id, full_name, email, phone, address FROM customers"
            )).mappings().all()

        best_score, best_row = 0, None
        for row in rows:
            score = fuzz.token_sort_ratio(name, row["full_name"].lower())
            if email and email == row["email"].lower():
                score = 100
            if score > best_score:
                best_score, best_row = score, row

        if best_row and best_score >= 75:
            result = dict(best_row)
            result["match"] = True
            result["match_score"] = best_score
            return json.dumps(result, default=str)

        return json.dumps({"match": False})
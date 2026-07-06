import json
import logging
from fastapi import FastAPI, HTTPException
from app.schemas import ReconcileRequest, ReconcileResponse
from app.crew import build_crew

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Multi-Agent Data Reconciliation & Formatting Engine",
    description="CrewAI-powered pipeline for extracting, validating, and formatting records against SQL Server.",
    version="1.0.0",
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/reconcile", response_model=ReconcileResponse)
def reconcile(payload: ReconcileRequest):
    results = []
    for raw in payload.raw_records:
        try:
            crew = build_crew(raw)
            output = crew.kickoff()
            parsed = json.loads(str(output))
            results.append(parsed)
        except Exception as e:
            logger.exception("Reconciliation failed for record")
            raise HTTPException(status_code=500, detail=str(e))
    return {"results": results}
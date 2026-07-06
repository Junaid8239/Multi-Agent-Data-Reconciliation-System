from pydantic import BaseModel
from typing import List, Optional

class ReconcileRequest(BaseModel):
    raw_records: List[str]

class ReconciledRecord(BaseModel):
    input_name: Optional[str] = None
    input_email: Optional[str] = None
    input_phone: Optional[str] = None
    matched_in_db: bool
    customer_id: Optional[int] = None
    canonical_name: Optional[str] = None
    canonical_email: Optional[str] = None
    canonical_phone: Optional[str] = None
    canonical_address: Optional[str] = None
    match_confidence: int = 0

class ReconcileResponse(BaseModel):
    results: List[ReconciledRecord]
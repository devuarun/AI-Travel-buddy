from pydantic import BaseModel
from typing import Dict, Any

class SearchQuery(BaseModel):
    origin: str
    destination: str
    dates: Dict[str, str]
    user_prefs: Dict[str, Any] = {}

class ReserveRequest(BaseModel):
    option_id: str
    pax: Dict[str, Any]

class PaymentRequest(BaseModel):
    tentative_id: str
    payment_info: Dict[str, Any]

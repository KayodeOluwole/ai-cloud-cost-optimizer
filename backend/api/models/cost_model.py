from pydantic import BaseModel
from datetime import date

class CostRecord(BaseModel):
    resource_id: str
    cost_amount: float
    usage_date: date

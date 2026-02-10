from pydantic import BaseModel
from datetime import datetime

class ExpenseCreate(BaseModel):
    title: str
    amount: float
    category: str

class ExpenseResponse(ExpenseCreate):
    id: int
    date: datetime

    class Config:
        from_attributes = True
from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

class Payment(BaseModel):
    session_id: int
    amount: Decimal
    method_id: int
    time: datetime

class PaymentCreate(BaseModel):
    session_id: int
    amount: Optional[Decimal] = None
    method_id: int
    time: datetime

class PaymentUpdate(BaseModel):
    session_id: Optional[int] = None
    amount: Optional[Decimal] = None
    method_id: Optional[int] = None
    time: Optional[datetime] = None

class PaymentOut(Payment):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

class RevenueReport(BaseModel):
    total_revenue: Decimal
    period_start: datetime
    period_end: datetime

class SessionsReport(BaseModel):
    total_sessions: int
    period_start: datetime
    period_end: datetime

class AverageCheckReport(BaseModel):
    average_check: Decimal
    period_start: datetime
    period_end: datetime

class DashboardData(BaseModel):
    total_revenue: Decimal
    total_sessions: int
    average_check: Decimal
    active_sessions: int
    free_spaces: int
    revenue_by_period: List[dict]
    sessions_by_period: List[dict]


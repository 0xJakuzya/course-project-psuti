from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from typing import Optional

from app.core.db import get_db
from app.modules.reports.schemas import RevenueReport, SessionsReport, AverageCheckReport, DashboardData
from app.modules.reports import utils

router = APIRouter(prefix='/reports', tags=['Reports'])

@router.get('/revenue', response_model=RevenueReport)
async def get_revenue(
    start_date: Optional[datetime] = Query(None, description="Начальная дата периода"),
    end_date: Optional[datetime] = Query(None, description="Конечная дата периода"),
    db: AsyncSession = Depends(get_db)):
    total_revenue = await utils.get_revenue(start_date, end_date, db)

    return RevenueReport(
        total_revenue=total_revenue,
        period_start=start_date or datetime.min,
        period_end=end_date or datetime.utcnow()
    )

@router.get('/sessions', response_model=SessionsReport)
async def get_sessions(
    start_date: Optional[datetime] = Query(None, description="Начальная дата периода"),
    end_date: Optional[datetime] = Query(None, description="Конечная дата периода"),
    db: AsyncSession = Depends(get_db)):
    total_sessions = await utils.get_sessions_count(start_date, end_date, db)

    return SessionsReport(
        total_sessions=total_sessions,
        period_start=start_date or datetime.min,
        period_end=end_date or datetime.utcnow()
    )

@router.get('/average-check', response_model=AverageCheckReport)
async def get_average_check(
    start_date: Optional[datetime] = Query(None, description="Начальная дата периода"),
    end_date: Optional[datetime] = Query(None, description="Конечная дата периода"),
    db: AsyncSession = Depends(get_db)):
    average_check = await utils.get_average_check(start_date, end_date, db)

    return AverageCheckReport(
        average_check=average_check,
        period_start=start_date or datetime.min,
        period_end=end_date or datetime.utcnow()
    )

@router.get('/dashboard', response_model=DashboardData)
async def get_dashboard(
    period: str = Query('day', description="Период: day, week, month"),
    db: AsyncSession = Depends(get_db)):
    try:
        if period not in ['day', 'week', 'month']:
            period = 'day'
        data = await utils.get_dashboard_data(period, db)

        return DashboardData(**data)

    except Exception as e:
        from fastapi import HTTPException, status
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при получении данных дашборда: {str(e)}"
        )


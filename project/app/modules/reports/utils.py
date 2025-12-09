from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, cast, Date
from datetime import datetime, timedelta, date
from decimal import Decimal
from typing import Optional, List

from app.models.parking_session import ParkingSession
from app.models.parking_space import ParkingSpace
from app.models.payments import Payment


async def get_revenue(start_date: Optional[datetime], end_date: Optional[datetime], db: AsyncSession) -> Decimal:
    query = select(ParkingSession).where(
        ParkingSession.time_out.isnot(None),
        ParkingSession.total_cost.isnot(None))
    if start_date:
        query = query.where(
            (ParkingSession.time_in <= end_date if end_date else True) &
            (ParkingSession.time_out >= start_date if start_date else True)
        )
    if end_date:
        query = query.where(ParkingSession.time_in <= end_date)
    result = await db.execute(query)
    sessions = result.scalars().all()
    total_revenue = Decimal('0')
    for session in sessions:
        session_start = session.time_in
        session_end = session.time_out
        if start_date and session_end < start_date:
            continue
        if end_date and session_start > end_date:
            continue
        if session.total_cost:
            total_revenue += Decimal(str(session.total_cost))
    
    return total_revenue


async def get_sessions_count(start_date: Optional[datetime], end_date: Optional[datetime], db: AsyncSession) -> int:
    query = select(func.count(ParkingSession.id))
    
    if start_date:
        query = query.where(ParkingSession.time_in >= start_date)
    if end_date:
        query = query.where(ParkingSession.time_in <= end_date)
    
    result = await db.execute(query)
    return result.scalar() or 0


async def get_average_check(start_date: Optional[datetime], end_date: Optional[datetime], db: AsyncSession) -> Decimal:
    query = select(ParkingSession).where(
        ParkingSession.time_out.isnot(None),
        ParkingSession.total_cost.isnot(None))
    
    if start_date:
        query = query.where(
            (ParkingSession.time_in <= end_date if end_date else True) &
            (ParkingSession.time_out >= start_date if start_date else True)
        )
    if end_date:
        query = query.where(ParkingSession.time_in <= end_date)
    
    result = await db.execute(query)
    sessions = result.scalars().all()
    
    if not sessions:
        return Decimal('0')
    
    total_cost = sum(Decimal(str(s.total_cost)) for s in sessions if s.total_cost)
    avg = total_cost / len(sessions) if sessions else Decimal('0')
    
    return avg


async def get_active_sessions_count(db: AsyncSession) -> int:
    query = select(func.count(ParkingSession.id)).where(ParkingSession.time_out.is_(None))
    result = await db.execute(query)
    return result.scalar() or 0


async def get_free_spaces_count(db: AsyncSession) -> int:
    all_spaces_query = select(func.count(ParkingSpace.id))
    all_spaces_result = await db.execute(all_spaces_query)
    total_spaces = all_spaces_result.scalar() or 0
    occupied_spaces_query = select(func.count(func.distinct(ParkingSession.space_id))).where(
        ParkingSession.time_out.is_(None))
    occupied_spaces_result = await db.execute(occupied_spaces_query)
    occupied_spaces = occupied_spaces_result.scalar() or 0
    
    return total_spaces - occupied_spaces


async def get_revenue_by_period(period: str, db: AsyncSession) -> List[dict]:
    now = datetime.utcnow()
    try:
        if period == 'day':
            filter_start = now - timedelta(days=7)
        elif period == 'week':
            filter_start = now - timedelta(weeks=12)
        else:
            filter_start = now - timedelta(days=365)

        query = select(ParkingSession).where(
            ParkingSession.time_out.isnot(None),
            ParkingSession.total_cost.isnot(None),
            (ParkingSession.time_in <= now) &
            (ParkingSession.time_out >= filter_start))
        
        result = await db.execute(query)
        sessions = result.scalars().all()
        revenue_by_period = {}
        
        for session in sessions:
            if not session.time_out or not session.total_cost:
                continue
            
            session_start = session.time_in
            session_end = session.time_out
            total_cost = float(session.total_cost)
            if period == 'day':
                current_date = session_start.date()
                end_date = session_end.date()
                while current_date <= end_date:
                    period_key = current_date.isoformat()
                    day_start_dt = datetime.combine(current_date, datetime.min.time())
                    day_end_dt = datetime.combine(current_date, datetime.max.time().replace(hour=23, minute=59, second=59, microsecond=999999))
                    period_start = max(session_start, day_start_dt)
                    period_end = min(session_end, day_end_dt)
                    
                    if period_start < period_end:
                        day_duration = (period_end - period_start).total_seconds()
                        total_duration = (session_end - session_start).total_seconds()
                        day_cost = total_cost * (day_duration / total_duration) if total_duration > 0 else 0
                        if period_key not in revenue_by_period:
                            revenue_by_period[period_key] = 0
                        revenue_by_period[period_key] += day_cost
                    current_date += timedelta(days=1)

            elif period == 'week':
                current = session_start
                while current <= session_end:
                    week_start = current - timedelta(days=current.weekday())
                    week_start = week_start.replace(hour=0, minute=0, second=0, microsecond=0)
                    week_end = week_start + timedelta(days=7)
                    period_start = max(session_start, week_start)
                    period_end = min(session_end, week_end)
                    if period_start < period_end:
                        period_duration = (period_end - period_start).total_seconds()
                        total_duration = (session_end - session_start).total_seconds()
                        period_cost = total_cost * (period_duration / total_duration) if total_duration > 0 else 0
                        period_key = week_start.isoformat()
                        if period_key not in revenue_by_period:
                            revenue_by_period[period_key] = 0
                        revenue_by_period[period_key] += period_cost
                    current = week_end
                    
            else:
                current = session_start
                while current <= session_end:
                    month_start = current.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
                    if month_start.month == 12:
                        month_end = month_start.replace(year=month_start.year + 1, month=1)
                    else:
                        month_end = month_start.replace(month=month_start.month + 1)
                    period_start = max(session_start, month_start)
                    period_end = min(session_end, month_end)
                    if period_start < period_end:
                        period_duration = (period_end - period_start).total_seconds()
                        total_duration = (session_end - session_start).total_seconds()
                        period_cost = total_cost * (period_duration / total_duration) if total_duration > 0 else 0
                        period_key = month_start.isoformat()
                        if period_key not in revenue_by_period:
                            revenue_by_period[period_key] = 0
                        revenue_by_period[period_key] += period_cost
                    current = month_end
        data = [{'period': k, 'revenue': round(v, 2)} for k, v in revenue_by_period.items()]
        data.sort(key=lambda x: x['period'])

        return data
    except Exception as e:
        import traceback
        print(f"Ошибка в get_revenue_by_period: {e}")
        print(traceback.format_exc())
        return []


async def get_sessions_by_period(period: str, db: AsyncSession) -> List[dict]:
    now = datetime.utcnow()
    try:
        if period == 'day':
            start_date = now - timedelta(days=7)
            query = select(
                cast(ParkingSession.time_in, Date).label('date'),
                func.count(ParkingSession.id).label('count')
            ).where(
                ParkingSession.time_in >= start_date
            ).group_by(cast(ParkingSession.time_in, Date)).order_by(cast(ParkingSession.time_in, Date))
        elif period == 'week':
            start_date = now - timedelta(weeks=12)
            query = select(
                func.date_trunc('week', ParkingSession.time_in).label('week'),
                func.count(ParkingSession.id).label('count')
            ).where(
                ParkingSession.time_in >= start_date
            ).group_by(func.date_trunc('week', ParkingSession.time_in)).order_by(func.date_trunc('week', ParkingSession.time_in))
        else:  # month
            start_date = now - timedelta(days=365)
            query = select(
                func.date_trunc('month', ParkingSession.time_in).label('month'),
                func.count(ParkingSession.id).label('count')
            ).where(
                ParkingSession.time_in >= start_date
            ).group_by(func.date_trunc('month', ParkingSession.time_in)).order_by(func.date_trunc('month', ParkingSession.time_in))
        
        result = await db.execute(query)
        rows = result.all()
        
        data = []
        for row in rows:
            if period == 'day':
                period_value = row.date
                if period_value:
                    if isinstance(period_value, (datetime, date)):
                        period_str = period_value.isoformat()
                    else:
                        period_str = str(period_value)
                else:
                    period_str = None
                data.append({
                    'period': period_str,
                    'count': row.count or 0
                })
            elif period == 'week':
                period_value = row.week
                if period_value:
                    if isinstance(period_value, (datetime, date)):
                        period_str = period_value.isoformat()
                    else:
                        period_str = str(period_value)
                else:
                    period_str = None
                data.append({
                    'period': period_str,
                    'count': row.count or 0
                })
            else:
                period_value = row.month
                if period_value:
                    if isinstance(period_value, (datetime, date)):
                        period_str = period_value.isoformat()
                    else:
                        period_str = str(period_value)
                else:
                    period_str = None
                data.append({
                    'period': period_str,
                    'count': row.count or 0
                })
        
        return data
    except Exception as e:
        # В случае ошибки возвращаем пустой список
        return []


async def get_dashboard_data(period: str, db: AsyncSession) -> dict:
    now = datetime.utcnow()
    
    # Определяем период для метрик
    if period == 'day':
        start_date = now - timedelta(days=1)
    elif period == 'week':
        start_date = now - timedelta(days=7)
    else:  # month
        start_date = now - timedelta(days=30)
    
    total_revenue = await get_revenue(start_date, now, db)
    total_sessions = await get_sessions_count(start_date, now, db)
    average_check = await get_average_check(start_date, now, db)
    active_sessions = await get_active_sessions_count(db)
    free_spaces = await get_free_spaces_count(db)
    revenue_by_period = await get_revenue_by_period(period, db)
    sessions_by_period = await get_sessions_by_period(period, db)
    
    return {
        'total_revenue': float(total_revenue),
        'total_sessions': total_sessions,
        'average_check': float(average_check),
        'active_sessions': active_sessions,
        'free_spaces': free_spaces,
        'revenue_by_period': revenue_by_period,
        'sessions_by_period': sessions_by_period
    }


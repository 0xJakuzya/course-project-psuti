from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from app.models.payments import Payment
from app.models.parking_session import ParkingSession
from app.modules.payments.schemas import PaymentCreate, PaymentUpdate
from typing import Optional


def to_naive_datetime(dt: datetime) -> datetime:
    if dt is None:
        return None
    if dt.tzinfo is not None:
        return dt.replace(tzinfo=None)
    return dt

async def create_payment(data: PaymentCreate, db: AsyncSession) -> Optional[Payment]:
    try:

        session = await db.get(ParkingSession, data.session_id)
        if not session:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Сессия парковки не найдена"
            )
        amount = data.amount
        if amount is None:
            if session.total_cost is None:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Сумма платежа не указана и не может быть получена из сессии (total_cost не установлен)"
                )
            amount = session.total_cost
        
        db_payment = Payment(
            session_id=data.session_id,
            amount=amount,
            method_id=data.method_id,
            time=to_naive_datetime(data.time)
        )
        db.add(db_payment)
        await db.commit()
        await db.refresh(db_payment)
        return db_payment
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании платежа: {str(e)}"
        )

async def get_payment_id(db: AsyncSession, payment_id: int) -> Optional[Payment]:
    payment = await db.get(Payment, payment_id)
    return payment

async def update_payment(db: AsyncSession, payment_id: int, data: PaymentUpdate) -> Optional[Payment]:
    payment = await get_payment_id(db, payment_id)
    if not payment:
        return None
    if data.session_id is not None:
        payment.session_id = data.session_id
    if data.amount is not None:
        payment.amount = data.amount
    if data.method_id is not None:
        payment.method_id = data.method_id
    if data.time is not None:
        payment.time = to_naive_datetime(data.time)
    db.add(payment)
    await db.commit()
    await db.refresh(payment)
    return payment


from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.modules.payments.schemas import PaymentCreate, PaymentUpdate, PaymentOut
from app.modules.payments import utils

from app.models import Payment

router = APIRouter(prefix='/payments', tags=['Payments'])

@router.post('/', response_model=PaymentOut, status_code=status.HTTP_200_OK)
async def create_payment(data: PaymentCreate, db: AsyncSession = Depends(get_db)):
    payment = await utils.create_payment(data, db)
    return PaymentOut.model_validate(payment)

@router.get('/', response_model=list[PaymentOut])
async def get_payments(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Payment))
    payments = result.scalars().all()
    return payments

@router.get('/{payment_id}', response_model=PaymentOut)
async def get_payment(payment_id: int, db: AsyncSession = Depends(get_db)):
    payment = await utils.get_payment_id(db, payment_id)
    if not payment:
        raise HTTPException(404, 'Payment not found')
    return payment

@router.put('/{payment_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_payment(payment_id: int, data: PaymentUpdate, db: AsyncSession = Depends(get_db)):
    payment = await utils.update_payment(db, payment_id, data)
    if not payment:
        raise HTTPException(404, 'Payment not found')
    return payment


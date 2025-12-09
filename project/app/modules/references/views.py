from fastapi import APIRouter, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.modules.references.schemas import VehicleTypeOut, PaymentMethodOut
from app.models import VehicleType, PaymentMethod

router = APIRouter(prefix='/references', tags=['References'])

@router.get('/vehicle-types', response_model=list[VehicleTypeOut])
async def get_vehicle_types(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(VehicleType))
    vehicle_types = result.scalars().all()
    return vehicle_types

@router.get('/payment-methods', response_model=list[PaymentMethodOut])
async def get_payment_methods(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(PaymentMethod))
    payment_methods = result.scalars().all()
    return payment_methods


from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
import math
from datetime import datetime
from decimal import Decimal

from app.models.parking_space import ParkingSpace
from app.models.tariff import Tariff
from app.models.parking_session import ParkingSession
from app.modules.parking.schemas import (
    ParkingSpaceCreate, ParkingSpaceUpdate,
    TariffCreate, TariffUpdate,
    ParkingSessionCreate, ParkingSessionUpdate
)
from typing import Optional

def to_naive_datetime(dt: datetime) -> datetime:
    if dt is None:
        return None
    if dt.tzinfo is not None:
        return dt.replace(tzinfo=None)
    return dt


async def create_parking_space(data: ParkingSpaceCreate, db: AsyncSession) -> Optional[ParkingSpace]:
    try:
        db_parking_space = ParkingSpace(
            number=data.number,
            type_id=data.type_id
        )
        db.add(db_parking_space)
        await db.commit()
        await db.refresh(db_parking_space)
        return db_parking_space
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании парковочного места: {str(e)}"
        )

async def get_parking_space_id(db: AsyncSession, parking_space_id: int) -> Optional[ParkingSpace]:
    parking_space = await db.get(ParkingSpace, parking_space_id)
    return parking_space

async def update_parking_space(db: AsyncSession, parking_space_id: int, data: ParkingSpaceUpdate) -> Optional[ParkingSpace]:
    parking_space = await get_parking_space_id(db, parking_space_id)
    if not parking_space:
        return None
    if data.number is not None:
        parking_space.number = data.number
    if data.type_id is not None:
        parking_space.type_id = data.type_id
    db.add(parking_space)
    await db.commit()
    await db.refresh(parking_space)
    return parking_space

async def delete_parking_space(db: AsyncSession, parking_space_id: int) -> bool:
    parking_space = await get_parking_space_id(db, parking_space_id)
    if not parking_space:
        return False
    await db.delete(parking_space)
    await db.commit()
    return True

async def create_tariff(data: TariffCreate, db: AsyncSession) -> Optional[Tariff]:
    try:
        db_tariff = Tariff(
            name=data.name,
            price_per_hour=data.price_per_hour,
            price_per_day=data.price_per_day)
        db.add(db_tariff)
        await db.commit()
        await db.refresh(db_tariff)
        return db_tariff
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании тарифа: {str(e)}"
        )

async def get_tariff_id(db: AsyncSession, tariff_id: int) -> Optional[Tariff]:
    tariff = await db.get(Tariff, tariff_id)
    return tariff

async def update_tariff(db: AsyncSession, tariff_id: int, data: TariffUpdate) -> Optional[Tariff]:
    tariff = await get_tariff_id(db, tariff_id)
    if not tariff:
        return None
    if data.name is not None:
        tariff.name = data.name
    if data.price_per_hour is not None:
        tariff.price_per_hour = data.price_per_hour
    if data.price_per_day is not None:
        tariff.price_per_day = data.price_per_day
    db.add(tariff)
    await db.commit()
    await db.refresh(tariff)
    return tariff

async def delete_tariff(db: AsyncSession, tariff_id: int) -> bool:
    tariff = await get_tariff_id(db, tariff_id)
    if not tariff:
        return False
    await db.delete(tariff)
    await db.commit()
    return True

async def create_parking_session(data: ParkingSessionCreate, db: AsyncSession) -> Optional[ParkingSession]:
    try:
        time_in = to_naive_datetime(data.time_in)
        time_out = to_naive_datetime(data.time_out) if data.time_out else None
        db_session = ParkingSession(
            vehicle_id=data.vehicle_id,
            space_id=data.space_id,
            tariff_id=data.tariff_id,
            time_in=time_in,
            time_out=time_out)
        if time_out and time_in:
            try:
                db_session.total_cost = await calculate_parking_cost(
                    time_in,
                    time_out,
                    data.tariff_id,
                    db
                )
            except HTTPException as e:
                await db.rollback()
                raise e
        
        db.add(db_session)
        await db.commit()
        await db.refresh(db_session)
        return db_session
    except HTTPException:
        raise
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании сессии парковки: {str(e)}"
        )

async def get_parking_session_id(db: AsyncSession, session_id: int) -> Optional[ParkingSession]:
    session = await db.get(ParkingSession, session_id)
    return session

async def calculate_parking_cost(time_in: datetime, time_out: datetime, tariff_id: int, db: AsyncSession) -> Decimal:
    time_in_naive = to_naive_datetime(time_in)
    time_out_naive = to_naive_datetime(time_out)
    if time_out_naive <= time_in_naive:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Время выхода должно быть позже времени входа"
        )
    tariff = await get_tariff_id(db, tariff_id)
    if not tariff:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Тариф не найден"
        )
    time_diff = time_out_naive - time_in_naive
    hours = time_diff.total_seconds() / 3600
    hours_rounded = math.ceil(hours)
    cost = Decimal(str(hours_rounded)) * Decimal(str(tariff.price_per_hour))
    
    return cost

async def update_parking_session(db: AsyncSession, session_id: int, data: ParkingSessionUpdate) -> Optional[ParkingSession]:
    session = await get_parking_session_id(db, session_id)
    if not session:
        return None
    if data.vehicle_id is not None:
        session.vehicle_id = data.vehicle_id
    if data.space_id is not None:
        session.space_id = data.space_id
    if data.tariff_id is not None:
        session.tariff_id = data.tariff_id
    if data.time_in is not None:
        session.time_in = to_naive_datetime(data.time_in)
    if data.time_out is not None:
        session.time_out = to_naive_datetime(data.time_out)
        # Автоматически рассчитываем стоимость, если time_out установлен и total_cost не передан
        if data.total_cost is None and session.time_out and session.time_in:
            try:
                session.total_cost = await calculate_parking_cost(
                    session.time_in, 
                    session.time_out, 
                    session.tariff_id, 
                    db
                )
            except HTTPException:
                pass

    if data.total_cost is not None:
        session.total_cost = data.total_cost
    db.add(session)
    await db.commit()
    await db.refresh(session)
    return session


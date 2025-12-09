from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.vehicles import Vehicle
from app.modules.vehicles.schemas import VehicleCreate, VehicleUpdate
from typing import Optional

async def create_vehicle(data: VehicleCreate, db: AsyncSession) -> Optional[Vehicle]:
    try:
        db_vehicle = Vehicle(
            brand=data.brand,
            model=data.model,
            license_plate=data.license_plate,
            color=data.color,
            type_id=data.type_id,
            client_id=data.client_id
        )
        db.add(db_vehicle)
        await db.commit()
        await db.refresh(db_vehicle)
        return db_vehicle
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании транспортного средства: {str(e)}"
        )

async def get_vehicle_id(db: AsyncSession, vehicle_id: int) -> Optional[Vehicle]:
    vehicle = await db.get(Vehicle, vehicle_id)
    return vehicle

async def update_vehicle(db: AsyncSession, vehicle_id: int, data: VehicleUpdate) -> Optional[Vehicle]:
    vehicle = await get_vehicle_id(db, vehicle_id)
    if not vehicle:
        return None
    if data.brand is not None:
        vehicle.brand = data.brand
    if data.model is not None:
        vehicle.model = data.model
    if data.license_plate is not None:
        vehicle.license_plate = data.license_plate
    if data.color is not None:
        vehicle.color = data.color
    if data.type_id is not None:
        vehicle.type_id = data.type_id
    if data.client_id is not None:
        vehicle.client_id = data.client_id
    db.add(vehicle)
    await db.commit()
    await db.refresh(vehicle)
    return vehicle

async def delete_vehicle(db: AsyncSession, vehicle_id: int) -> bool:
    vehicle = await get_vehicle_id(db, vehicle_id)
    if not vehicle:
        return False
    await db.delete(vehicle)
    await db.commit()
    return True


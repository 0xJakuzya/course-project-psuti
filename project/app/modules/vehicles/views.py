from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.modules.vehicles.schemas import VehicleCreate, VehicleUpdate, VehicleOut
from app.modules.vehicles import utils

from app.models import Vehicle

router = APIRouter(prefix='/vehicles', tags=['Vehicles'])

@router.post('/', response_model=VehicleOut, status_code=status.HTTP_200_OK)
async def create_vehicle(data: VehicleCreate, db: AsyncSession = Depends(get_db)):
    vehicle = await utils.create_vehicle(data, db)
    return VehicleOut.model_validate(vehicle)

@router.get('/', response_model=list[VehicleOut])
async def get_vehicles(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Vehicle))
    vehicles = result.scalars().all()
    return vehicles

@router.get('/{vehicle_id}', response_model=VehicleOut)
async def get_vehicle(vehicle_id: int, db: AsyncSession = Depends(get_db)):
    vehicle = await utils.get_vehicle_id(db, vehicle_id)
    if not vehicle:
        raise HTTPException(404, 'Vehicle not found')
    return vehicle

@router.put('/{vehicle_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_vehicle(vehicle_id: int, data: VehicleUpdate, db: AsyncSession = Depends(get_db)):
    vehicle = await utils.update_vehicle(db, vehicle_id, data)
    if not vehicle:
        raise HTTPException(404, 'Vehicle not found')
    return vehicle

@router.delete('/{vehicle_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_vehicle(vehicle_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await utils.delete_vehicle(db, vehicle_id)
    if not deleted:
        raise HTTPException(404, 'Vehicle not found')
    return None


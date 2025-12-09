from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.modules.parking.schemas import (
    ParkingSpaceCreate, ParkingSpaceUpdate, ParkingSpaceOut,
    TariffCreate, TariffUpdate, TariffOut,
    ParkingSessionCreate, ParkingSessionUpdate, ParkingSessionOut
)
from app.modules.parking import utils

from app.models import ParkingSpace, Tariff, ParkingSession

router = APIRouter(prefix='/parking-spaces', tags=['Parking Spaces'])
tariff_router = APIRouter(prefix='/tariffs', tags=['Tariffs'])
session_router = APIRouter(prefix='/parking-sessions', tags=['Parking Sessions'])

@router.post('/', response_model=ParkingSpaceOut, status_code=status.HTTP_200_OK)
async def create_parking_space(data: ParkingSpaceCreate, db: AsyncSession = Depends(get_db)):
    parking_space = await utils.create_parking_space(data, db)
    return ParkingSpaceOut.model_validate(parking_space)

@router.get('/', response_model=list[ParkingSpaceOut])
async def get_parking_spaces(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ParkingSpace))
    parking_spaces = result.scalars().all()
    return parking_spaces

@router.get('/{parking_space_id}', response_model=ParkingSpaceOut)
async def get_parking_space(parking_space_id: int, db: AsyncSession = Depends(get_db)):
    parking_space = await utils.get_parking_space_id(db, parking_space_id)
    if not parking_space:
        raise HTTPException(404, 'Parking space not found')
    return parking_space

@router.put('/{parking_space_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_parking_space(parking_space_id: int, data: ParkingSpaceUpdate, db: AsyncSession = Depends(get_db)):
    parking_space = await utils.update_parking_space(db, parking_space_id, data)
    if not parking_space:
        raise HTTPException(404, 'Parking space not found')
    return parking_space

@router.delete('/{parking_space_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_parking_space(parking_space_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await utils.delete_parking_space(db, parking_space_id)
    if not deleted:
        raise HTTPException(404, 'Parking space not found')
    return None

# Tariff routes
@tariff_router.post('/', response_model=TariffOut, status_code=status.HTTP_200_OK)
async def create_tariff(data: TariffCreate, db: AsyncSession = Depends(get_db)):
    tariff = await utils.create_tariff(data, db)
    return TariffOut.model_validate(tariff)

@tariff_router.get('/', response_model=list[TariffOut])
async def get_tariffs(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Tariff))
    tariffs = result.scalars().all()
    return tariffs

@tariff_router.get('/{tariff_id}', response_model=TariffOut)
async def get_tariff(tariff_id: int, db: AsyncSession = Depends(get_db)):
    tariff = await utils.get_tariff_id(db, tariff_id)
    if not tariff:
        raise HTTPException(404, 'Tariff not found')
    return tariff

@tariff_router.put('/{tariff_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_tariff(tariff_id: int, data: TariffUpdate, db: AsyncSession = Depends(get_db)):
    tariff = await utils.update_tariff(db, tariff_id, data)
    if not tariff:
        raise HTTPException(404, 'Tariff not found')
    return tariff

@tariff_router.delete('/{tariff_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_tariff(tariff_id: int, db: AsyncSession = Depends(get_db)):
    deleted = await utils.delete_tariff(db, tariff_id)
    if not deleted:
        raise HTTPException(404, 'Tariff not found')
    return None

# ParkingSession routes (без DELETE)
@session_router.post('/', response_model=ParkingSessionOut, status_code=status.HTTP_200_OK)
async def create_parking_session(data: ParkingSessionCreate, db: AsyncSession = Depends(get_db)):
    session = await utils.create_parking_session(data, db)
    return ParkingSessionOut.model_validate(session)

@session_router.get('/', response_model=list[ParkingSessionOut])
async def get_parking_sessions(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(ParkingSession))
    sessions = result.scalars().all()
    return sessions

@session_router.get('/{session_id}', response_model=ParkingSessionOut)
async def get_parking_session(session_id: int, db: AsyncSession = Depends(get_db)):
    session = await utils.get_parking_session_id(db, session_id)
    if not session:
        raise HTTPException(404, 'Parking session not found')
    return session

@session_router.put('/{session_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_parking_session(session_id: int, data: ParkingSessionUpdate, db: AsyncSession = Depends(get_db)):
    session = await utils.update_parking_session(db, session_id, data)
    if not session:
        raise HTTPException(404, 'Parking session not found')
    return session


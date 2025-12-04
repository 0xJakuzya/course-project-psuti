from fastapi import APIRouter, Depends, status, HTTPException
from fastapi.params import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.modules.clients.schemas import ClientsCreate, ClientsUpdate, ClientsOut
from app.modules.clients import utils

from app.models import Client

router = APIRouter(prefix='/clients', tags=['Clients'])

@router.post('/', response_model=ClientsOut, status_code=status.HTTP_200_OK)
async def create_clients(data: ClientsCreate, db: AsyncSession = Depends(get_db)):
    client = await utils.create_clients(data, db)
    return ClientsOut.model_validate(client)

@router.get('/', response_model=list[ClientsOut])
async def get_clients(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Client))
    clients = result.scalars().all()
    return clients

@router.get('/{clients_id}', response_model=ClientsOut)
async def get_client(clients_id: int, db: AsyncSession = Depends(get_db)):
    clients = await utils.get_client_id(db, clients_id)
    return clients

@router.put('/{clients_id}', status_code=status.HTTP_204_NO_CONTENT)
async def update_clients(clients_id: int, data: ClientsUpdate,db: AsyncSession = Depends(get_db)):
    clients = await utils.update_clients(db, clients_id, data)
    if not clients:
        raise HTTPException(404, 'Client not found')
    return clients

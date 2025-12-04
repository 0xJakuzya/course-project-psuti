from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.clients import Client
from app.modules.clients.schemas import ClientsCreate, ClientsUpdate
from typing import Optional, List


async def create_clients(data: ClientsCreate, db: AsyncSession) -> Optional[Client]:
    try:
        db_client = Client(name=data.name, surname=data.surname, phone=data.phone)
        db.add(db_client)
        await db.commit()
        await db.refresh(db_client)
        return db_client
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ошибка при создании клиента: {str(e)}"
        )

async def get_client_id(db: AsyncSession, client_id: int) -> Optional[Client]:
    client = await db.get(Client, client_id)
    return client

async def update_clients(db: AsyncSession, clients_id: int, data: ClientsUpdate) -> Optional[Client]:
    clients = await get_client_id(db, clients_id)
    if not clients:
        return None
    if data.name is not None:
        clients.name = data.name
    if data.surname is not None:
        clients.surname = data.surname
    if data.phone is not None:
        clients.phone = data.phone
    db.add(clients)
    await db.commit()
    await db.refresh(clients)
    return clients

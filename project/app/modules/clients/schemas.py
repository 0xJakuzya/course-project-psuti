from pydantic import BaseModel
from typing import Optional

class Clients(BaseModel):
    name: str
    surname: str
    phone: str

class ClientsCreate(Clients):
    pass

class ClientsUpdate(BaseModel):
    name: Optional[str] = None
    surname: Optional[str] = None
    phone: Optional[str] = None

class ClientsOut(Clients):
    id: int

    class Config:
        from_attributes = True


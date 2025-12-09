from pydantic import BaseModel
from typing import Optional

class Vehicle(BaseModel):
    brand: str
    model: str
    license_plate: str
    color: str
    type_id: int
    client_id: int

class VehicleCreate(Vehicle):
    pass

class VehicleUpdate(BaseModel):
    brand: Optional[str] = None
    model: Optional[str] = None
    license_plate: Optional[str] = None
    color: Optional[str] = None
    type_id: Optional[int] = None
    client_id: Optional[int] = None

class VehicleOut(Vehicle):
    id: int

    class Config:
        from_attributes = True


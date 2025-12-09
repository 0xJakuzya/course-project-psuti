from pydantic import BaseModel
from typing import Optional
from datetime import datetime
from decimal import Decimal

# ParkingSpace schemas
class ParkingSpace(BaseModel):
    number: str
    type_id: int

class ParkingSpaceCreate(ParkingSpace):
    pass

class ParkingSpaceUpdate(BaseModel):
    number: Optional[str] = None
    type_id: Optional[int] = None

class ParkingSpaceOut(ParkingSpace):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Tariff schemas
class Tariff(BaseModel):
    name: str
    price_per_hour: Decimal
    price_per_day: Decimal

class TariffCreate(Tariff):
    pass

class TariffUpdate(BaseModel):
    name: Optional[str] = None
    price_per_hour: Optional[Decimal] = None
    price_per_day: Optional[Decimal] = None

class TariffOut(Tariff):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# ParkingSession schemas
class ParkingSession(BaseModel):
    vehicle_id: int
    space_id: int
    tariff_id: int
    time_in: datetime
    time_out: Optional[datetime] = None
    total_cost: Optional[Decimal] = None

class ParkingSessionCreate(BaseModel):
    vehicle_id: int
    space_id: int
    tariff_id: int
    time_in: datetime
    time_out: Optional[datetime] = None

class ParkingSessionUpdate(BaseModel):
    vehicle_id: Optional[int] = None
    space_id: Optional[int] = None
    tariff_id: Optional[int] = None
    time_in: Optional[datetime] = None
    time_out: Optional[datetime] = None
    total_cost: Optional[Decimal] = None

class ParkingSessionOut(ParkingSession):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


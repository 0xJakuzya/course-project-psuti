from pydantic import BaseModel

class VehicleTypeOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True

class PaymentMethodOut(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


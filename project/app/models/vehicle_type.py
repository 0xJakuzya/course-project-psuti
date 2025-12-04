from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.db import Base

class VehicleType(Base):
    __tablename__ = "vehicle_types"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)

    vehicles = relationship("Vehicle", back_populates="vehicle_type")
    parking_spaces = relationship("ParkingSpace", back_populates="vehicle_type")
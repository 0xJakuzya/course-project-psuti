from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from project.app.core.db import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    license_plate = Column(String(20), nullable=False, unique=True)
    color = Column(String(30), nullable=False)
    type_id = Column(Integer, ForeignKey("vehicle_types.id"), nullable=False)
    client_id = Column(Integer, ForeignKey("clients.id"), nullable=False)

    vehicle_type = relationship("VehicleType", back_populates="vehicles")
    client = relationship("Client", back_populates="vehicles")
    parking_sessions = relationship("ParkingSession", back_populates="vehicle")
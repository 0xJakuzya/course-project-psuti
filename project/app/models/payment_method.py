from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from project.app.core.db import Base

class PaymentMethod(Base):
    __tablename__ = "payment_methods"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)

    payments = relationship("Payment", back_populates="payment_method")
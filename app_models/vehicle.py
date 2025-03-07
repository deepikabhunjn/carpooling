from sqlalchemy import Column, Integer, String, ForeignKey
from db import Base

class Vehicle(Base):
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    make = Column(String(50), nullable=False)
    model = Column(String(50), nullable=False)
    license_plate = Column(String(20), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"))
    image_link = Column(String(255))  
    available_seat = Column(Integer, nullable=False)  #  available seats
    vehicle_type = Column(String(50), nullable=False)  # vehicle type (e.g., SUV, Van)

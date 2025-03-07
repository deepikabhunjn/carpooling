from sqlalchemy import Column, Integer, Float, String, DateTime, Boolean, ForeignKey
from db import Base
from datetime import datetime

class Trip(Base):# creating the trips table storing details of the trips created by a user and vehicle used when trip s
    __tablename__ = "trips"

    id = Column(Integer, primary_key=True, index=True)
    pickup_location = Column(String(255), nullable=False)
    drop_location = Column(String(255), nullable=False)
    date = Column(DateTime, nullable=False, default=datetime.utcnow)
    seats_available = Column(Integer, nullable=False)
    price = Column(Float, nullable=False)
    ride_fare = Column(Float)
    estimated_time = Column(String(20))
    is_completed = Column(Boolean, default=False)
    is_canceled = Column(Boolean, default=False)
    status = Column(String(20), default="Scheduled")
    
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Reference to the driver (user)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)  # Reference to the vehicle

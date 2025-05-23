from sqlalchemy import Column, Integer, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from db import Base
from datetime import datetime

# when user books a ride, data is stored in this table with trip_id, passengerid being user id,pickup location id from start
# destination id from destination, 
class RideBooking(Base):
    __tablename__ = "ride_bookings"
    id = Column(Integer, primary_key=True, index=True)
    trip_id = Column(Integer, ForeignKey("trips.id"), nullable=False)
    passenger_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    pickup_location_id = Column(Integer, ForeignKey("start.id"), nullable=False)
    drop_location_id = Column(Integer, ForeignKey("destinations.id"), nullable=False)
    confirmed = Column(Boolean, default=False)
    booked_at = Column(DateTime, default=datetime.utcnow)
    passenger = relationship("User", foreign_keys=[passenger_id])
    pickup_location = relationship("Start",foreign_keys=[pickup_location_id],)
    drop_location = relationship("Destination", foreign_keys=[drop_location_id])


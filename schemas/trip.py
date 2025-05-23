from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TripBase(BaseModel):
    pickup_location: str
    drop_location: str
    date: datetime
    seats_available: int
    price: float
    ride_fare: Optional[float] = None
    estimated_time: Optional[str] = None

class TripCreate(TripBase):
    user_id: int  # Driver ID
    vehicle_id: int  # Vehicle ID

class TripUpdate(BaseModel):
    is_completed: Optional[bool] = None
    is_canceled: Optional[bool] = None
    status: Optional[str] = None

class TripOut(TripBase):
    id: int
    user_id: int
    vehicle_id: int
    status: str
    is_completed: bool
    is_canceled: bool

    class Config:
        from_attributes = True

# schema for returning trips with driver and vehicle details
class TripDetailOut(TripOut):
    driver_name: str
    driver_profile_picture: Optional[str]
    vehicle_type: str
    vehicle_image: Optional[str]
    driver_overall_rating: Optional[float] = None

class TripSeatUpdate(BaseModel):
    seats_available: int
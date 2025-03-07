from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class UserDetail(BaseModel):
    id: int
    profile_picture: Optional[str] = None
    full_name: str

    class Config:
        from_attributes = True

class DestinationDetail(BaseModel):
    id: int
    latitude: float
    longitude: float

    class Config:
        from_attributes = True

class StartDetail(BaseModel):
    id: int
    location_name: str
    latitude: float
    longitude: float

    class Config:
        from_attributes = True

class RideBookingDetail(BaseModel):
    id: int
    passenger: UserDetail
    pickup_location: StartDetail
    drop_location: DestinationDetail
    confirmed: bool
    booked_at: datetime

    class Config:
        from_attributes = True

class RideBookingBase(BaseModel):
    trip_id: int
    passenger_id: int
    pickup_location_id: int
    drop_location_id: int
    confirmed: Optional[bool] = False

class RideBookingCreate(RideBookingBase):
    pass

class RideBookingOut(RideBookingBase):
    id: int
    booked_at: datetime

    class Config:
        from_attributes = True

class RideBookingUpdate(BaseModel):
    confirmed: bool

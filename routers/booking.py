from typing import Dict, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import booking as ride_booking_crud
from schemas.booking import RideBookingDetail, RideBookingCreate, RideBookingOut, RideBookingUpdate
from db import get_db

router = APIRouter()

# retrieving booking id for a given trip id and user id,find passenger row(id),then find booking row for passeger
@router.get("/ride_bookings/trip/booking_id/{trip_id}/{user_id}", response_model=Dict[str, int])
def get_booking_id_by_trip_and_user(trip_id: int, user_id: int, db: Session = Depends(get_db)):
    booking = ride_booking_crud.get_booking_id_by_trip_and_user(db, trip_id, user_id)
    if not booking:
        raise HTTPException(status_code=404, detail="Booking not found for the given trip and user")
    return {"booking_id": booking.id}

# return all bookings for a particular trip id
@router.get("/trips/{trip_id}", response_model=List[RideBookingDetail])
def get_trip_bookings(trip_id: int, db: Session = Depends(get_db)):
    bookings = ride_booking_crud.get_ride_bookings_by_trip(db, trip_id)
    if not bookings:
        raise HTTPException(status_code=404, detail="No bookings found for this trip")
    return bookings

# create a booking
@router.post("/ride_bookings/", response_model=RideBookingOut)
def create_ride_booking(ride_booking: RideBookingCreate, db: Session = Depends(get_db)):
    return ride_booking_crud.create_ride_booking(db, ride_booking)

# update booking - cancel by rider - confirmed - false
@router.put("/ride_bookings/{booking_id}", response_model=RideBookingOut)
def update_ride_booking( booking_id: int,booking_update: RideBookingUpdate, db: Session = Depends(get_db),):
    confirmed = booking_update.confirmed
    db_ride_booking = ride_booking_crud.update_ride_booking(db, booking_id, confirmed)
    if db_ride_booking is None:
        raise HTTPException(status_code=404, detail="Booking not found")
    return db_ride_booking
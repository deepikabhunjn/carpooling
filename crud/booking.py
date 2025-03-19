from sqlalchemy.orm import Session,joinedload
from app_models.booking import RideBooking
from app_models.passenger import Passenger
from schemas.booking import RideBookingCreate
from app_models.user import User 

def get_booking_id_by_trip_and_user(db: Session, trip_id: int, user_id: int):
    """
    1) Find the passenger record where user_id = user_id and trip_id = trip_id.
    2) Use passenger.id to find the matching RideBooking record in ride_bookings.
    3) Return that RideBooking (or None if not found).
    """
    # Step 1: Find passenger row
    passenger = db.query(Passenger).filter(
        Passenger.user_id == user_id, 
        Passenger.trip_id == trip_id
    ).first()

    if not passenger:
        return None  # Means no passenger record found for this user/trip

    # Step 2: Use passenger.id to find the booking
    booking = db.query(RideBooking).filter(
        RideBooking.trip_id == trip_id,
        RideBooking.passenger_id == passenger.id
    ).first()

    return booking

#create booking
def create_ride_booking(db: Session, ride_booking: RideBookingCreate):    
    db_ride_booking = RideBooking(**ride_booking.dict())
    db.add(db_ride_booking)
    db.commit()
    db.refresh(db_ride_booking)
    return db_ride_booking

# get all ride bookings associated with a specific trip_id
def get_ride_bookings_by_trip(db: Session, trip_id: int):
    return db.query(RideBooking).options(
        joinedload(RideBooking.passenger),
        joinedload(RideBooking.pickup_location),
        joinedload(RideBooking.drop_location)
    ).filter(RideBooking.trip_id == trip_id).all()


# Get a ride booking by ID
def get_ride_booking(db: Session, booking_id: int):
    return db.query(RideBooking).filter(RideBooking.id == booking_id).first()

# Update a ride booking (e.g., confirmation status)
def update_ride_booking(db: Session, booking_id: int, confirmed: bool):
    db_ride_booking = get_ride_booking(db, booking_id)
    if db_ride_booking:
        db_ride_booking.confirmed = confirmed
        db.commit()
        db.refresh(db_ride_booking)
    return db_ride_booking





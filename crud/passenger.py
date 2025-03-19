from sqlalchemy.orm import Session
from app_models.passenger import Passenger
from schemas.passenger import PassengerCreate

def create_passenger(db: Session, passenger: PassengerCreate):
    db_passenger = Passenger(**passenger.dict())
    db.add(db_passenger)
    db.commit()
    db.refresh(db_passenger)
    return db_passenger



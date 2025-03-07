from sqlalchemy.orm import Session
from app_models.vehicle import Vehicle
from schemas.vehicle import VehicleCreate

# create an instance of vehicle and store in db
def create_vehicle(db: Session, vehicle: VehicleCreate):
    db_vehicle = Vehicle(**vehicle.dict())
    db.add(db_vehicle)
    db.commit()
    db.refresh(db_vehicle)
    return db_vehicle

# get vehicle details through vehicle id
def get_vehicle(db: Session, vehicle_id: int):
    return db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

# get vehivles by user id 
def get_vehicles_by_user(db: Session, user_id: int):
    return db.query(Vehicle).filter(Vehicle.user_id == user_id).all()



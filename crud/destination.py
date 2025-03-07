from sqlalchemy.orm import Session
from app_models.destination import Destination
from schemas.destination import DestinationCreate

def create_destination(db: Session, destination: DestinationCreate):
    db_destination = Destination(**destination.dict())
    db.add(db_destination)
    db.commit()
    db.refresh(db_destination)
    return db_destination



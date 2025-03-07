from sqlalchemy.orm import Session
from app_models.start import Start
from schemas.start import StartCreate

def create_start(db: Session, start: StartCreate):
    db_start = Start(**start.dict())
    db.add(db_start)
    db.commit()
    db.refresh(db_start)
    return db_start

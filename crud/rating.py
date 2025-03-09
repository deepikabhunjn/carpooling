from sqlalchemy.orm import Session
from app_models.rating import Rating
from schemas.rating import RatingCreate

def create_rating(db: Session, rating: RatingCreate):
    db_rating = Rating(**rating.dict())
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)
    return db_rating

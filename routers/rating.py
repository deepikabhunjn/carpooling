from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud import rating as rating_crud
from schemas import rating as rating_schemas
from db import get_db

router = APIRouter()

@router.post("/ratings/", response_model=rating_schemas.RatingOut)
def create_rating(rating: rating_schemas.RatingCreate, db: Session = Depends(get_db)):
    return rating_crud.create_rating(db, rating)


from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from crud import destination as destination_crud
from schemas import destination as destination_schemas
from db import get_db

router = APIRouter()

@router.post("/destinations/", response_model=destination_schemas.DestinationOut)
def create_destination(destination: destination_schemas.DestinationCreate, db: Session = Depends(get_db)):
    return destination_crud.create_destination(db, destination)


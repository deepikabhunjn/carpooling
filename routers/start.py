from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import start as start_crud
from schemas import start as start_schemas
from db import get_db

router = APIRouter()

@router.post("/starts/", response_model=start_schemas.StartOut)
def create_start(start: start_schemas.StartCreate, db: Session = Depends(get_db)):
    return start_crud.create_start(db, start)


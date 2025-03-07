from sqlalchemy import Column, Integer, String, Float
from db import Base

#creating a start table to store the current location details of rider from google map api 
class Start(Base):
    __tablename__ = "start"
    
    id = Column(Integer, primary_key=True, index=True)
    location_name = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
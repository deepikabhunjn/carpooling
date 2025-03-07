from sqlalchemy import Column, Integer, String, Float
from db import Base

#creating a destination table to store the drop off details of rider from google map api 
class Destination(Base):
    __tablename__ = "destinations"
    
    id = Column(Integer, primary_key=True, index=True)
    location_name = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
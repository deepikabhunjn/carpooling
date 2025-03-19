from sqlalchemy import Column, Integer, String, Float
from db import Base

# price of car type depends - so for a ride created the price defers - calculation of fare
class VehiclePricing(Base):
    __tablename__ = "vehicle_pricings"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_type = Column(String(50), unique=True, index=True, nullable=False)  
    rate_per_km = Column(Float, nullable=False)
from fastapi import FastAPI
from db import engine
# import all models - tables 
from app_models import (
    user as user_models,
    booking as booking_models,
    trip as trip_models,
    destination as destination_models,
    vehicle as vehicle_models,
    rating as rating_models,
    passenger as passenger_models,
    start as start_models,
    vehicle_pricing as pricing_models,
)

# Import routers
from routers import (
    user as user_router,
    booking as booking_router,
    trip as trip_router,
    destination as destination_router,
    vehicle as vehicle_router,
    rating as rating_router,
    passenger as passenger_router,
    start as start_router,
    vehicle_pricing as pricing_router,
)

# Create database tables
user_models.Base.metadata.create_all(bind=engine)
booking_models.Base.metadata.create_all(bind=engine)
trip_models.Base.metadata.create_all(bind=engine)
destination_models.Base.metadata.create_all(bind=engine)
vehicle_models.Base.metadata.create_all(bind=engine)
passenger_models.Base.metadata.create_all(bind=engine)
start_models.Base.metadata.create_all(bind=engine)
rating_models.Base.metadata.create_all(bind=engine)
pricing_models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Include routers
app.include_router(user_router.router, prefix="/users", tags=["users"])
app.include_router(booking_router.router, prefix="/bookings", tags=["bookings"])
app.include_router(trip_router.router, prefix="/trips", tags=["trips"])
app.include_router(destination_router.router, prefix="/destinations", tags=["destinations"])
app.include_router(vehicle_router.router, prefix="/vehicles", tags=["vehicles"])
app.include_router(passenger_router.router, prefix="/passengers", tags=["passengers"])
app.include_router(start_router.router, prefix="/starts", tags=["starts"])
app.include_router(rating_router.router, prefix="/ratings", tags=["ratings"])
app.include_router(pricing_router.router, prefix="/pricing", tags=["pricing"])

@app.get("/")
def read_root():
    return {"message": "Carpooling API is running"}

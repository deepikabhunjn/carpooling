from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from db import engine
from app_models import user as user_models
from app_models import booking as booking_models
from app_models import trip as trip_models
from app_models import destination as destination_models
from app_models import vehicle as vehicle_models
from app_models import rating as rating_models
from app_models import passenger as passenger_models
from app_models import start as start_models  # Add start_models to import

from routers import user as user_router
from routers import booking as booking_router
from routers import trip as trip_router
from routers import destination as destination_router
from routers import vehicle as vehicle_router  # Rename for clarity
from routers import rating as rating_router
from routers import passenger as passenger_router
from routers import start as start_router  # Add start_router to import

# Create database tables
user_models.Base.metadata.create_all(bind=engine)
booking_models.Base.metadata.create_all(bind=engine)
trip_models.Base.metadata.create_all(bind=engine)
destination_models.Base.metadata.create_all(bind=engine)
vehicle_models.Base.metadata.create_all(bind=engine)
passenger_models.Base.metadata.create_all(bind=engine)
start_models.Base.metadata.create_all(bind=engine)  # Create start table

app = FastAPI()


app.include_router(user_router.router, prefix="/users", tags=["users"])
app.include_router(booking_router.router, prefix="/bookings", tags=["bookings"])
app.include_router(trip_router.router, prefix="/trips", tags=["trips"])
app.include_router(destination_router.router, prefix="/destinations", tags=["destinations"])
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")
app.include_router(vehicle_router.router, prefix="/vehicles", tags=["vehicles"])  # Vehicles router
app.include_router(passenger_router.router, prefix="/passengers", tags=["passengers"])# Vehicle pricing router
app.include_router(start_router.router, prefix="/starts", tags=["starts"])  # Include start router


@app.get("/")
def read_root():
    return {"message": "Carpooling API is running"}
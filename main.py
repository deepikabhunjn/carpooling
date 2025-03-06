from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from db import engine
from app_models import user as user_models


from routers import user as user_router


# Create database tables
user_models.Base.metadata.create_all(bind=engine)


app = FastAPI()

# Include routers

app.include_router(user_router.router, prefix="/users", tags=["users"])



@app.get("/")
def read_root():
    return {"message": "Carpooling API is running"}
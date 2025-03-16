# carpooling backend

Carpooling Backend
The Carpooling Backend is a FastAPI-based project designed to support a carpooling service. It provides RESTful APIs for managing users, bookings, trips, vehicles, ratings, passengers, and other related entities. This backend serves as the foundation for carpooling applications, managing drivers, passengers, and their trips efficiently.

Features
User management (riders and drivers)
Trip creation and booking system
Vehicle and driver registration
Passenger tracking for each trip
Rating system for trips and passengers

Technologies
Python 3.9+
FastAPI - Web framework for creating APIs
SQLAlchemy - ORM for database management
Pydantic - Data validation and parsing
MySQL (or any relational database supported by SQLAlchemy)
Project Structure
carpooling/
        app_models/
        crud/
        routers/
        schemas/
        suggestion/
        db.py
        main.py

Installation and Setup
Clone the repository:

git clone https://github.com/deepikabhunjn/carpooling.git

cd carpooling

python -m venv venv source venv/bin/activate # On Windows use venv\Scripts\activate

pip install -r requirements.txt

run

uvicorn main:app --reload
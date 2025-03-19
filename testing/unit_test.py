import pytest
from fastapi.testclient import TestClient
from db import engine, SessionLocal, Base
from main import app  # Import the FastAPI app instance
# Create a fixture to get the TestClient
@pytest.fixture(scope="module")
def client():
    # Setup the database
    Base.metadata.create_all(bind=engine)  # Create tables for testing
    client = TestClient(app)
    yield client

    #Cleanup the database after tests are done
    Base.metadata.drop_all(bind=engine)


# Fixture to get a testing database session
@pytest.fixture(scope="module")
def db():
    db = SessionLocal()
    yield db
    db.close()

# Sample Test Case for User Registration
def test_create_user(client, db):
    # Define the payload for creating a user
    user_data = {
        "email": "testuser@example.com",
        "full_name": "Test User",
        "password": "password123",
        "is_driver": False,
        "nic_number": "",
        "license_number": ""
    }
    
    # Send POST request to the "/users/" endpoint
    response = client.post("/users/users/", json=user_data)
    
    # Assert response status code and content
    assert response.status_code == 201
    assert response.json()["email"] == user_data["email"]

# Test case for login route
def test_login_user(client, db):
    user_data = {
        "email": "testuser@example.com",
        "password": "password123"
    }
    
    # Register the user first to test the login
    client.post("/users/users/", json=user_data)
    
    # Send POST request to login
    response = client.post("/users/login/", data={"username": user_data["email"], "password": user_data["password"]})
    
    # Assert response status code and content
    assert response.status_code == 200
    assert "id" in response.json()

# Test case for getting user by ID
def test_read_user(client, db):
    # Assume a user with ID 1 exists
    response = client.get("/users/users/1")
    
    # Assert response status code and content
    assert response.status_code == 200
    assert "id" in response.json()


# Sample Test Case for creating a vehicle without an image
def test_create_vehicle_without_image(client):
    response = client.post(
        "/vehicles/vehicles/",
        json={
            "make": "Toyota",
            "model": "Corolla",
            "license_plate": "ABC123",
            "user_id": 1,
            "available_seat": 4,
            "vehicle_type": "Sedan",
            "image_link": None
        },
    )
    assert response.status_code == 200


def test_create_trip(client):
    # Create trip data
    trip_data = {
        "pickup_location": "Location A",
        "drop_location": "Location B",
        "date": "2025-02-24T10:00:00",
        "seats_available": 3,
        "price": 50.0,
        "ride_fare": 45.0,
        "estimated_time": "1 hour",
        "user_id": 1,
        "vehicle_id": 1
    }

    # Create trip
    response = client.post("/trips/trips/", json=trip_data)
    
    # Assert the response status code and data
    assert response.status_code == 200
    trip = response.json()
    assert trip["pickup_location"] == "Location A"
    assert trip["drop_location"] == "Location B"
    assert trip["seats_available"] == 3
    assert trip["price"] == 50.0

def test_create_passenger(client):
    # Create trip data
    passenger_data = {
        "user_id": 1,
        "trip_id": 1,
        "status": "Pending",
        "created_at": "01/04/25"
    }

    # Create trip
    response = client.post("/passengers/passengers/", json=passenger_data)
    
    # Assert the response status code and data
    assert response.status_code == 200
    passenger = response.json()
    assert passenger["user_id"] == 1
    assert passenger["status"] == "Pending"
    assert passenger["trip_id"] == 1

def test_create_start_location(client):
    # Create start location data
    response = client.post("/starts/starts/", json={
        "location_name": "Location A",
        "latitude": 0,
        "longitude": 0
    })
    # Assert the response status code and data
    assert response.status_code == 200
    start_location = response.json()
    assert start_location["location_name"] == "Location A"
    assert start_location["latitude"] == 0
    assert start_location["longitude"] == 0


def test_create_destination_location(client):
    # Create start location data
    destination_location_data = {
        "location_name": "Location B",
        "latitude": 1.0,
        "longitude": 1.0
    }
    response = client.post("/destinations/destinations/", json=destination_location_data)
    
    # Assert the response status code and data
    assert response.status_code == 200
    destination_location = response.json()
    assert destination_location["location_name"] == "Location B"
    assert destination_location["latitude"] == 1.0
    assert destination_location["longitude"] == 1.0

def test_booking(client):
    # Create booking data
    booking_data = {    
        "trip_id": 1,
        "passenger_id" :1,
        "pickup_location_id": 1,
        "drop_location_id": 1,
        "confirmed": 0,
    }
    response = client.post("/bookings/ride_bookings/", json=booking_data)
     # Assert the response status code and data
    assert response.status_code == 200
    booking = response.json()
    assert booking["trip_id"] == 1
    assert booking["passenger_id"] == 1
    assert booking["confirmed"] == 0

def test_get_trips_driver(client):  
     # Assume a user with ID 1 exists
    response = client.get("/trips/trips/driver/1") 
    # Assert response status code and content
    assert response.status_code == 200
    trips = response.json()
    assert isinstance(trips, list)
    for trip in trips:
        assert "user_id" in trip
        assert trip["user_id"] == 1

def test_update_trip(client):
    trip_data = {
        "is_completed": 1,
        "is_canceled": 0,
        "status": "Pending"
    }
    response = client.put("/trips/trips/1", json=trip_data)
    
    # Assert response status code and content
    assert response.status_code == 200
    assert response.json()["is_completed"] == trip_data["is_completed"]

def test_get_trips_rider(client):
      # Assume a user with ID 1 exists
    response = client.get("/trips/trips/rider/1") 
    # Assert response status code and content
    assert response.status_code == 200
    trips = response.json()
    assert isinstance(trips, list)
    for trip in trips:
        assert "user_id" in trip
        assert trip["user_id"] == 1

    
def test_get_bookings_trip(client):
    response = client.get("/bookings/trips/1")
    assert response.status_code == 200
    trips = response.json()
    assert isinstance(trips, list)
    for trip in trips:
        assert "confirmed" in trip
        assert trip["confirmed"] == 0    

def test_create_rating(client):
    rating_data= {
        "trip_id": 1,
        "rated_by_user_id": 1,
        "driver_id": 1,
        "rating": 1,
        "feedback": "Nice ride"
    }
    response = client.post("/ratings/ratings/", json=rating_data)
    # Assert the response status code and data
    assert response.status_code == 200
    rating = response.json()
    assert rating["trip_id"] == 1
    assert rating["rated_by_user_id"] == 1
    assert rating["driver_id"] == 1
    assert rating["rating"] == 1
    assert rating["feedback"] == "Nice ride"
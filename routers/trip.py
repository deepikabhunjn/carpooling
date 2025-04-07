import torch
import torch.nn as nn
import torch.nn.functional as F
import numpy as np
from collections import defaultdict
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from transformers import BertTokenizer, BertModel
from typing import List
from app_models.passenger import Passenger
from app_models.trip import Trip
from app_models.user import User
from app_models.vehicle import Vehicle
from app_models.rating import Rating
from schemas import trip as trip_schemas
from db import get_db
from crud import trip as trip_crud

router = APIRouter()
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
tokenizer = BertTokenizer.from_pretrained('bert-base-uncased') # for tokenizer

# Sentiment Analysis Model
class Sentiment(nn.Module):
    def __init__(self):
        super(Sentiment, self).__init__()
        self.bert = BertModel.from_pretrained('bert-base-uncased') # extract word embeddings
        self.lstm = nn.LSTM(768, 128, batch_first=True, bidirectional=True) # 125 hidden units - captures sequential dependencies
        self.fc = nn.Linear(256, 2) # fully connected layers - 2 classes positive/negative
    
    def forward(self, input_ids, attention_mask):
        with torch.no_grad():
            embeddings = self.bert(input_ids, attention_mask)[0] # extract embeddings
        lstm_out, _ = self.lstm(embeddings) # passes embeddings through LSTM
        out = torch.cat((lstm_out[:, -1, :128], lstm_out[:, 0, 128:]), dim=1) #Concatenates first and last LSTM hidden states
        return self.fc(out) # output logits

# Load trained model
model = Sentiment()
model.load_state_dict(torch.load('./suggestion/bert_lstm_sentiment_model3.pth', map_location=device))
model.to(device)
model.eval()

# Sentiment scoring function
def get_sentiment_score(text):
    encoded = tokenizer(text, return_tensors='pt', padding=True, truncation=True, max_length=256) #tokenize input
    input_ids, attention_mask = encoded['input_ids'].to(device), encoded['attention_mask'].to(device) # run sentiment model inference
    
    with torch.no_grad():
        logits = model(input_ids, attention_mask)
        probs = F.softmax(logits, dim=1)# applies softmax to logits to get probabilities
    
    sentiment_score = probs[0][1].item() - probs[0][0].item() # difference between prob to get sentiment score
    scaled_rating = max(1.0, min(5.0, 1 + 4 * ((sentiment_score + 1) / 2))) # scale 1-5
    return scaled_rating

@router.get("/suggestion/", response_model=list[trip_schemas.TripDetailOut])
def get_all_trips(db: Session = Depends(get_db)):
    trips_query = (
        # get all trip details with driver and vehicle details
        db.query(Trip, User.full_name, User.profile_picture, Vehicle.vehicle_type, Vehicle.image_link) .join(User, Trip.user_id == User.id).join(Vehicle, Trip.vehicle_id == Vehicle.id) .all() )
    
    if not trips_query:
        return []
    # fetch the ratings of each driver
    all_ratings = db.query(Rating).all()
    driver_scores = defaultdict(list)
    
    for row in all_ratings:
        if row.feedback:
            rating = get_sentiment_score(row.feedback) # compute sentiment score (1-5)
            driver_scores[row.driver_id].append((row.rating, rating)) # store scores in driver scores dictionary
    
    driver_predicted_ratings = {}
    
    for d_id, ratings in driver_scores.items():
        avg_numeric = np.mean([r[0] for r in ratings])
        avg_sentiment = np.mean([r[1] for r in ratings])
        # compute 70% numeric and 30% sentiment score
        driver_predicted_ratings[d_id] = avg_numeric * 0.7 + avg_sentiment * 0.3
    
    results = [
        trip_schemas.TripDetailOut(
            **trip.__dict__,
            driver_name=full_name,
            driver_profile_picture=profile_picture,
            vehicle_type=vehicle_type,
            vehicle_image=image_link,
            driver_overall_rating=driver_predicted_ratings.get(trip.user_id, None)
        )
        for trip, full_name, profile_picture, vehicle_type, image_link in trips_query
    ]
    
    return sorted(results, key=lambda x: (-x.driver_overall_rating if x.driver_overall_rating else 0)) # sort descending order


# get all the trips related to a passenger
@router.get("/trips/rider/{user_id}", response_model=List[trip_schemas.TripDetailOut])
def get_trips_by_rider(user_id: int, db: Session = Depends(get_db)):
    #  Find all Passenger records for the given rider (user)
    passenger_records = db.query(Passenger).filter(Passenger.user_id == user_id).all()
    if not passenger_records:
        raise HTTPException(status_code=404, detail="No passenger records found for this user.")
    # Extract unique trip IDs from these passenger records
    trip_ids = list({record.trip_id for record in passenger_records})
    # Step 3: Retrieve trip details joined with driver and vehicle information
    trips_with_details = (
        db.query(
            Trip,
            User.full_name,
            User.profile_picture,
            Vehicle.vehicle_type,
            Vehicle.image_link,
        )
        .join(User, Trip.user_id == User.id)
        .join(Vehicle, Trip.vehicle_id == Vehicle.id)
        .filter(Trip.id.in_(trip_ids))
        .all()
    )   
    if not trips_with_details:
        raise HTTPException(status_code=404, detail="No trips found for the given passenger records.")
    # Step 4: Map the results to the TripDetailOut schema
    results = []
    for trip, full_name, profile_picture, vehicle_type, image_link in trips_with_details:
        results.append(
            trip_schemas.TripDetailOut(
                **trip.__dict__,
                driver_name=full_name,
                driver_profile_picture=profile_picture,
                vehicle_type=vehicle_type,
                vehicle_image=image_link,
            ))
    return results

# Create a new trip
@router.post("/trips/", response_model=trip_schemas.TripOut)
def create_trip(trip: trip_schemas.TripCreate, db: Session = Depends(get_db)):
    return trip_crud.create_trip(db, trip)

# Get a trip by ID
@router.get("/trips/{trip_id}", response_model=trip_schemas.TripOut)
def read_trip(trip_id: int, db: Session = Depends(get_db)):
    db_trip = trip_crud.get_trip(db, trip_id)
    if db_trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    return db_trip

# Get trips by driver ID
@router.get("/trips/driver/{user_id}", response_model=list[trip_schemas.TripOut])
def get_trips_by_driver(user_id: int, db: Session = Depends(get_db)):
    return trip_crud.get_trips_by_driver(db, user_id)

@router.get("/trips/", response_model=list[trip_schemas.TripDetailOut])
def get_all_trips(db: Session = Depends(get_db)):
    trips = trip_crud.get_all_trips(db)
    return trips

# Update the seat availaibility
@router.put("/trips/seats/{trip_id}", response_model=trip_schemas.TripOut)
def update_trip_seats(trip_id: int, seat_update: trip_schemas.TripSeatUpdate, db: Session = Depends(get_db)):
    db_trip = trip_crud.update_seat_availability(db, trip_id, seat_update.seats_available)
    if not db_trip:
        raise HTTPException(status_code=404, detail="Trip not found")
    return db_trip

# Update a trip
@router.put("/trips/{trip_id}", response_model=trip_schemas.TripOut)
def update_trip(trip_id: int, trip_update: trip_schemas.TripUpdate, db: Session = Depends(get_db)):
    db_trip = trip_crud.update_trip(db, trip_id, trip_update)
    if db_trip is None:
        raise HTTPException(status_code=404, detail="Trip not found")
    return db_trip



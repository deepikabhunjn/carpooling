from db import Base  
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime

# creating users table in database -- storing user details.
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True) # id being the primary key
    full_name = Column(String(255), index=True)  # Added length for VARCHAR
    email = Column(String(255), unique=True, index=True)  
    password = Column(String(255))  
    is_driver = Column(Boolean, default=False)
    nic_number = Column(String(50), nullable=True)  
    license_number = Column(String(50), nullable=True)  
    profile_picture = Column(String(255), nullable=True) 
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User(id={self.id}, full_name='{self.full_name}', email='{self.email}')>"
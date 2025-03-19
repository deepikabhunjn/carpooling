from sqlalchemy.orm import Session
from app_models.user import User
from schemas.user import UserCreate
from passlib.context import CryptContext

#using bcrypt for hasing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Utility function to hash passwords
def get_password_hash(password: str):
    return pwd_context.hash(password)

# Get user by email
def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

# Create new user
def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(
        full_name=user.full_name,
        email=user.email,
        password=hashed_password,
        is_driver=user.is_driver,
        nic_number=user.nic_number,
        license_number=user.license_number
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Get user by ID
def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()
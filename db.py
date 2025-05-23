from sqlalchemy import create_engine 
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL Database URL
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:Deepika1010@localhost:3306/test"

# Create the engine to connect to the MySQL database
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for declarative models to inherit from
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()



import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from dotenv import load_dotenv

# load environment variables from .env file
load_dotenv()

# set up database
if os.getenv("TESTING"):
    DATABASE_URL = os.getenv("DATABASE_URL1")
else:
    DATABASE_URL = os.getenv("DATABASE_URL")

# create database engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# create database session
def init_db():
    from .models import Station  
    Base.metadata.create_all(bind=engine)

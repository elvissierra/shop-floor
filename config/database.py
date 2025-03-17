from sqlalchemy import create_engine
from sqlalchemy.engine import URL
from sqlalchemy.orm import sessionmaker
import os

url = URL.create(
    drivername= os.getenv("DB_NAME"),
    username= os.getenv("DB_USER"),
    password= os.getenv("DB_PASSWORD"),
    host= os.getenv("DB_HOST"),
    port= os.getenv("DB_PORT"),
)

engine = create_engine(url)
Session = sessionmaker(bind=engine)
session = Session()
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os
import pymysql
if os.path.exists("TodoApp/files.env"):
    load_dotenv("TodoApp/files.env")

DB_PASS = os.getenv("DB_PASS")

SQLALCHEMY_DATABASE_URL = 'sqlite:///./TodoApp/todosapp.db'

engine = create_engine(SQLALCHEMY_DATABASE_URL)

Base = declarative_base()  #Object of the database


SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
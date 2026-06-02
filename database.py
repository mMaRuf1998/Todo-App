from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from dotenv import load_dotenv
import os
load_dotenv("files.env")
DB_PASS = os.getenv("DB_PASS")

POSTGRESQL_DATABASE_URL = f"postgresql://postgres:{DB_PASS}@localhost/postgres"

engine = create_engine(POSTGRESQL_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()  #Object of the database

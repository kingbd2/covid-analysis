from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

COVID_DB_ENGINE_CONNECTION = os.getenv('COVID_DB_ENGINE_CONNECTION')
engine = create_engine(COVID_DB_ENGINE_CONNECTION, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
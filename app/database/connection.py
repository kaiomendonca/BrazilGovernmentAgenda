from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from app.core.dependencies import Base

DATABASE_URL = os.getenv("DATABASE_URL")

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)
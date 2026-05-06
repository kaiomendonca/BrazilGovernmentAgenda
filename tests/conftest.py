import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database.connection import Base


@pytest.fixture
def db_session():
    engine = create_engine("sqlite:///:memory:")
    
    SessionLocal = sessionmaker(bind=engine)
    
    session = SessionLocal()
    
    Base.metadata.create_all(bind=engine)
    
    yield session
    
    session.close()
import pytest
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from app.database.connection import Base


@pytest.fixture
def db_session():
    engine = create_engine("sqlite///:memory:")
    
    TestingSessionLocal = sessionmaker(bind=engine)
    
    Base.metadata.create_all(bind=engine)
    
    connection = engine.connect()
    transaction = connection.begin()
    session = TestingSessionLocal(bind=connection)
    
    yield session
    
    session.close()
    transaction.rollback()
    connection.close()
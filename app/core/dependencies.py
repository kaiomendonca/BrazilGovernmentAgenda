from app.database.connection import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


from sqlalchemy.orm import declarative_base

Base = declarative_base()
from app.database.connection import SessionLocal
from contextlib import contextmanager

@contextmanager
def get_db():
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()


from sqlalchemy.orm import declarative_base

Base = declarative_base()
from app.database.connection import Base
from sqlalchemy import Column, Integer, String, Enum
import enum


class PubliclyExposedPersons(str, enum.Enum):
    PRESIDENT = "presidente-da-republica"
    VICE_PRESIDENT = "vice-presidente"
    FIRST_LADY = "primeira-dama"
    

class Event(Base):
    __tablename__ = "events"

    _id = Column(Integer, primary_key=True, index=True)
    datetime = Column(String, index=True)
    href = Column(String, index=True)
    location = Column(String, index=True)
    start = Column(String, index=True)
    title = Column(String, index=True)
    

class Authorities(Base):
    __tablename__ = "authorities"

    _id = Column(Integer, primary_key=True, index=True)
    role = Column(Enum(PubliclyExposedPersons), index=True)
    event_id = Column(Integer, foreign_key = "events._id")
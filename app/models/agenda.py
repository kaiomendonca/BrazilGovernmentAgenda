from core.dependencies import Base
from sqlalchemy import Column, Integer, String, Date


class Event(Base):
    __tablename__ = "events"

    _id = Column(Integer, primary_key=True, index=True)
    datetime = Column(String, index=True)
    href = Column(String, index=True)
    location = Column(String, index=True)
    start = Column(String, index=True)
    title = Column(String, index=True)
    
    


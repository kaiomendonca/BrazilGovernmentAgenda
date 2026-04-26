from models.agenda import Event
from sqlalchemy.orm import Session


class EventRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, events):
        for event in events:
            
            exists = self.session.query(Event).filter_by(
                href=event["href"]
            ).first()

            if not exists:
                new_event = Event(**event)
                self.session.add(new_event)

        self.session.commit()
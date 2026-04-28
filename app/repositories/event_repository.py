from app.models.agenda import Event
from sqlalchemy.orm import Session


class EventRepository:
    def __init__(self, session: Session):
        self.session = session

    def save(self, events):
        
        event_fields = {'datetime', 'href', 'location', 'start', 'title'}
        
        for event in events:
            exists = self.session.query(Event).filter_by(
                href=event.get("href")
            ).first()

            if not exists:
                
                event_data = {k: v for k, v in event.items() if k in event_fields}
                new_event = Event(**event_data)
                self.session.add(new_event)

        self.session.commit()
        

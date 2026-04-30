from app.models.agenda import Event
from app.repositories.authority_repository import AuthorityRepository
from sqlalchemy.orm import Session


class EventRepository:
    def __init__(self, session: Session):
        self.session = session
        self.authority_repository = AuthorityRepository(session)

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
                self.session.flush()
                self.authority_repository.save_for_event(new_event, event.get("href"))
            else:
                self.authority_repository.save_for_event(exists, event.get("href"))

        self.session.commit()
        

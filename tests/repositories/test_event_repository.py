import pytest
from app.repositories.event_repository import EventRepository
from app.models.agenda import Event
from pytest_mock import MockerFixture

class TestEventRepository:
    
    def test_save_new_event(self, db_session, mocker: MockerFixture):
        repo = EventRepository(db_session)
        
        mock_authority = mocker.patch.object(
            repo.authority_repository,
            "save_for_event"
        )
        
        events = [
            {
            "href": "http://fake-url",
            "title": "Evento Teste",
            "datetime": "2026-03-02T09:00:00-03:00",
            "location": "Palácio da Alvorada",
            "start": "10h00"
            }
        ]
        
        repo.save(events)
        
        saved = db_session.query(Event).filter_by(href="http://fake-url").first()
        
        assert saved is not None
        assert saved.title == "Evento Teste"
        
        mock_authority.assert_called_once()


    def test_save_does_not_duplicate_event(self, db_session, mocker: MockerFixture):
        repo = EventRepository(db_session)
        
        existing = Event(
            href = "http://fake-url",
            title = "Evento Teste",
            datetime = "2026-03-02T09:00:00-03:00",
            location = "Palácio da Alvorada",
            start = "10h00"
        )
        
        db_session.add(existing)
        db_session.commit()
        
        
        mock_authority = mocker.patch.object(
            repo.authority_repository,
            "save_for_event"
        )
        
        
        events = [
            {
            "href": "http://fake-url",
            "title": "Evento Teste",
            "datetime": "2026-03-02T09:00:00-03:00",
            "location": "Palácio da Alvorada",
            "start": "10h00"
            }
        ]
        
        repo.save(events)
        
        results = db_session.query(Event).filter_by(href="http://fake-url").all()
        
        assert len(results) == 1
        
        mock_authority.assert_called_once()
        
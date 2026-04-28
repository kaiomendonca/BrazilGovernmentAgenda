from app.utils.date_utils import generate_dates
from app.utils.url_builder import build_official_url
from app.services.request_service import request_data
from app.repositories.event_repository import EventRepository
from app.core.dependencies import get_db
from app.database.connection import init_db


def process_agenda(official_name: str, start_date: str, end_date: str):
    
    init_db()
    
    date_list = generate_dates(start_date, end_date)

    for date in date_list:
        url = build_official_url(official_name, date)
        event_list = request_data(url)

        if event_list:
            with get_db() as db:
                repository = EventRepository(db)
                repository.save(event_list)
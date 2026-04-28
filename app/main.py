import click
from app.utils.date_utils import generate_dates
from app.utils.url_builder import build_official_url
from app.services.request_service import request_data
from app.repositories.event_repository import EventRepository
from app.core.dependencies import get_db
from app.database.connection import init_db
from dotenv import load_dotenv

load_dotenv()


@click.command()
@click.option("--name", prompt="president, vice_president, or first_lady")
@click.option("--first_date", prompt="start date")
@click.option("--second_date", prompt="end date")
def main(name, first_date, second_date):
    init_db()
    
    date_list = generate_dates(first_date, second_date)

    for date in date_list:
        url = build_official_url(name, date)

        event_list = request_data(url)
        if event_list:
            with get_db() as db:
                repository = EventRepository(db)
                repository.save(event_list)

if __name__ == "__main__":
    main()

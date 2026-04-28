import click
from app.services.agenda_service import process_agenda
from dotenv import load_dotenv

load_dotenv()


@click.command()
@click.option("--name", prompt="president, vice_president, or first_lady")
@click.option("--first_date", prompt="start date")
@click.option("--second_date", prompt="end date")
def main(name, first_date, second_date):
    process_agenda(name, first_date, second_date)

if __name__ == "__main__":
    main()

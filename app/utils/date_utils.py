from app.core.logger import logger
import click

def generate_dates(first_date: str, second_date: str) -> list:
    logger.info("Generating dates")
    from datetime import datetime, timedelta

    try:
        first_date_parse = datetime.strptime(first_date, "%Y-%m-%d")
        second_date_parse = datetime.strptime(second_date, "%Y-%m-%d")
    
    except ValueError:
        logger.error("Invalid date format or non-existent date")
        raise click.ClickException("Invalid date")

    day_difference = second_date_parse - first_date_parse
    
    if day_difference.days < 0:
        logger.error(
            "The first date must have occurred before the second date."
        )
        raise click.ClickException("Invalid date interval")

    date_list = []

    for day in range(day_difference.days + 1):
        
        date = (
            (first_date_parse + timedelta(days=day)).strftime("%Y-%m-%d")
        )
        date_list.append(date)
    logger.info(f"Generated {len(date_list)} dates")
    return date_list
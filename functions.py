import logging
import click

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


def generate_dates(first_date:str, second_date:str):
    logger.info("Generating dates")
    from datetime import datetime, timedelta

    first_date_parse = datetime.strptime(first_date, "%Y-%m-%d")
    second_date_parse = datetime.strptime(second_date, "%Y-%m-%d")

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

            



def request_data(url):
    logger.info(f"Requesting {url}")
    import requests
    import json
    
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": (
            "text/html,application/xhtml+xml,"
            "application/xml;q=0.9,image/avif,"
            "image/webp,image/apng,*/*;q=0.8"
        ),
        "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Referer": "https://www.google.com/",
        "Cache-Control": "max-age=0"
    }

    response = requests.get(url, headers= headers)

    for day in response.json():
        if day['isSelected'] == True:
            events = day['items']
            logger.info(f"Found {len(events)} events")
            return events
        

def get_mongo_client():
    from pymongo import MongoClient, errors
    import os

    connection_string = os.getenv("MONGO_URL")
    try:
        client = MongoClient(connection_string, serverSelectionTimeoutMS=5000)
        client.server_info()
        logger.info("Successful connection to MongoDB.")
        return client
    except errors.ServerSelectionTimeoutError:
        logger.error("Failed to connect to MongoDB. Please try again.")
        return None
        


def save_on_file(events):
    from pymongo import MongoClient, errors
    client = get_mongo_client()

    if client is None:
        logger.error("We were unable to connect to the database.")
        return
    
    logger.info("Connecting to the database...")
    database = client["GovernmentDB"]
    collection = database["Events"]
    logger.info("Persisting events in the database...")

    try:    
        for event in events:
            collection.insert_one(
                {
                    "datetime": event["datetime"],
                    "href": event["href"],
                    "location": event["location"],
                    "start": event["start"],
                    "title": event["title"],
                }
            )
        logger.info(f"{len(events)} events were saved")
    except errors.PyMongoError as error:
        logger.error(f"Failed to save event '{event['title']}': {error}")

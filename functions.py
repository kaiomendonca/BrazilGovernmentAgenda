import logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
)
logger = logging.getLogger(__name__)


def generate_dates(first_date:str, second_date:str):
    logger.info("Generating dates")
    from datetime import datetime, timedelta

    first_date_parse = datetime.strptime(first_date, "%d/%m/%Y")
    second_date_parse = datetime.strptime(second_date, "%d/%m/%Y")

    day_difference = second_date_parse - first_date_parse
    if day_difference.days < 0:
        print("Passe a data mais antiga, depois a data mais recente.")
        return 
    
    date_list = []

    for day in range(day_difference.days):
        
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
        



def save_on_file(events):
    logger.info("Saving on file")
    import csv

    with open("agenda.csv", "w", encoding= "utf8", newline='') as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                'Dia/Hora',
                'URL do evento',
                'Localização',
                'Horário de início',
                'Título' 
            ]
        )

        for event in events:
            writer.writerow(
                [   
                    event['datetime'],
                    event['href'],
                    event['location'],
                    event['start'],
                    event['title']
                ]
            )

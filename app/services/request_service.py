from app.core.logger import get_logger
import requests
logger = get_logger(__name__)

def request_data(url: str) -> list:
    logger.info(f"Requesting {url}")


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
        "Cache-Control": "max-age=0",
    }

    try:
        response = requests.get(url, headers=headers)
    
    except requests.exceptions.RequestException as error:
        logger.error(f"Request failed: {error}")
        return None

    for day in response.json():
        if day["isSelected"] == True:
            events = day["items"]
            logger.info(f"Found {len(events)} events")
            return events
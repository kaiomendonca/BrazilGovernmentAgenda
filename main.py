import requests
import json
from pprint import pprint
import csv
url = (
    "https://www.gov.br/planalto/pt-br/acompanhe-o-planalto"
    "/agenda-do-presidente-da-republica-lula/agenda-do-presidente-da-republica"
    "/json/2025-11-28"
)

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

response = requests.get(url, headers=headers)


for dia in response.json():
    if dia['isSelected'] == True:
        eventos = dia['items']


with open("agenda.csv", "w", encoding= "utf8", newline='') as arquivo:
    writer = csv.writer(arquivo)
    writer.writerow(
        [
            'Dia/Hora',
            'URL do evento',
            'Localização',
            'Horário de início',
            'Título' 
        ]
    )

    for evento in eventos:
        writer.writerow(
            [   
                evento['datetime'],
                evento['href'],
                evento['location'],
                evento['start'],
                evento['title']
            ]
        )

 

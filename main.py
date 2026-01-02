import requests
import json
import csv
from functions import generate_dates, request_data, save_on_file



def main(first_date, second_date):
    date_list = generate_dates(first_date, second_date)

    for date in date_list:
        url = (
            "https://www.gov.br/planalto/pt-br/acompanhe-o-planalto"
            "/agenda-do-presidente-da-republica-lula/agenda-do-presidente-da-republica"
            f"/json/{date}"
        )   
        event_list = request_data(url) 
        save_on_file(event_list)

if __name__ == "__main__":
    first_date = "06/12/2025"
    second_date = "10/12/2025"
    main(first_date, second_date)

 

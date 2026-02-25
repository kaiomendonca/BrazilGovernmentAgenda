import click
from functions import (
    generate_dates,
    request_data,
    save_on_file,
    build_official_url
) 
from dotenv import load_dotenv 

load_dotenv()
@click.command()
@click.option('--name', prompt='president, vice_president, or first_lady')
@click.option('--first_date', prompt='start date')
@click.option('--second_date', prompt='end date')
def main(name, first_date, second_date):
    date_list = generate_dates(first_date, second_date)

    for date in date_list:
        url = build_official_url(name,date)
            
    
        event_list = request_data(url) 
        save_on_file(event_list)

if __name__ == "__main__":
    main()

 

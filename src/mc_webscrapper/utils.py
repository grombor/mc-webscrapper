from datetime import datetime
import csv, sys
from random import randint as r
from time import sleep
from src.mc_webscrapper.errors import Error

# Main data holder
records = []
requests_timeout = 10



def get_date() -> str:
    return datetime.now().strftime("%d/%m/%Y")


def compare_prices(current_price=int, previous_price=int):
    try:
        if (current_price != '' and previous_price!=''):
            percent = str((int(current_price)*100 / int(previous_price))-100).split(".")
            return f"Cena zmieniła się o {percent[0]}%"
        raise Error()
    except Error as e:
        print(e, f"price change logic")
        return f""


def show_status(item, set):
    for i in range(len(set)):
        sys.stdout.write(f"Progress: {item} of {len(set)} \r")
        sys.stdout.flush()



def write_to_csv_file(name='results', test=False):

    if test:
        file_name = f"test_{name}.csv"
    else:
        file_name = f"{name}.csv"

    with open(file_name, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = [
            "DYSTRYBUTOR",
            "DATA",
            "MODEL",
            "ODPOWIEDNIK",
            "CENA KATALOGOWA NETTO",
            "CENA SKLEPU INTERNETOWEGO NETTO",
            "RABAT",
            "CENA KATALOGOWA PO RABACIE",
            "WYSOKOŚĆ",
            "SZEROKOŚĆ",
            "GŁĘBOKOŚĆ",
            "CECHY CHARAKTERYSTYCZNE",
            "ŹRÓDŁO",
            "CZAS REALIZACJI [dni]",
            "GWARANCJA [miesiące]",
            "msg"
        ]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        print('Printing to csv file...')
        writer.writeheader()

        for row in records:
            writer.writerow(row)



def wait(time=2):
    half_time = int(time*0.5)
    sleep(r(half_time, time))


def extract_digits(string) -> str:
    return ''.join([i for i in string if i.isdigit()])






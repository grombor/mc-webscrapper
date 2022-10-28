from datetime import datetime
import sys
from dataclasses import dataclass
from dataclass_csv import DataclassWriter
from mc_webscrapper.scrapper_dataclass import ScrapperDataClass


def show_status(item, set):
    print(set[item][0])
    sys.stdout.write(f"Scrapping: {item + 1} of {len(set)} \r")
    sys.stdout.flush()

def clear_price(nett_price: str) -> int:
    nett_price = nett_price.split(",")[0]
    return int(''.join([i for i in nett_price if i.isdigit()]))

def extract_digits(string: str) -> int:
    return int(''.join([i for i in string if i.isdigit()]))

def save_dataclass_to_file(name, list_dataclass):
    year = datetime.now().strftime("%Y")
    month = datetime.now().strftime("%m")
    filename = f"csv\\{year}-{month}-{name}.csv"
    with open(filename, "w", encoding="utf-8", newline='') as file:
        w = DataclassWriter(file, list_dataclass, ScrapperDataClass)
        w.write()
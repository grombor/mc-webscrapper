import sys
from dataclasses import dataclass
from dataclass_csv import DataclassWriter
from src.mc_webscrapper.scrapper_dataclass import ScrapperDataClass


def show_status(item, set):
    for i in range(len(set)):
        sys.stdout.write(f"Progress: {item} of {len(set)} \r")
        sys.stdout.flush()

def clear_price(nett_price: str) -> int:
    nett_price = nett_price.split(",")[0]
    return int(''.join([i for i in nett_price if i.isdigit()]))

def extract_digits(string: str) -> int:
    return int(''.join([i for i in string if i.isdigit()]))

def save_dataclass_to_file(filename, list_dataclass):
    with open(filename, "w", encoding="utf-8", newline='') as file:
        w = DataclassWriter(file, list_dataclass, ScrapperDataClass)
        w.write()
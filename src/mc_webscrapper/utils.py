from datetime import datetime
import csv
from random import randint as r
from time import sleep

# Main data holder
records = []


def get_date() -> str:
    return datetime.now().strftime("%d/%m/%Y")


def compare_prices(current_price=int, previous_price=int):
  try:
    percent = str((int(current_price)*100 / int(previous_price))-100).split(".")
    return f"Cena zmieniła się o {percent[0]}%"
    raise Error("")
  except Error as e:
    return f""


def write_to_csv_file(test=False):

  if test:
    file_name = 'test_results.txt'
  else:
    file_name = 'results.txt'

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


class Error(Exception):
    """Base class for other exceptions"""


    def __init__(self, msg):
        self.message = msg


    def __str__(self):
        return f"ERROR: {self.message}"




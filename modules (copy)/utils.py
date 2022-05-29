#TODO: nie nadpisywanie, a dopisywanie do pliku csv

import csv
from random import randint as r
from time import sleep

from numpy import integer

# Main data holder
records = []

def compare_prices(current_price, previous_price):
  try:
    percent = str((int(current_price)*100 / int(previous_price))-100).split(".")
    return percent[0]
  except:
    return "brak danych"


def write_to_csv_file():
  with open('test.csv', 'w', newline='', encoding='utf-8') as csvfile:
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

def wait(time=1):
  half_time = int(time*0.5)
  sleep(r(half_time, time))
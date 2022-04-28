#TODO: nie nadpisywanie, a dopisywanie do pliku csv

import csv

# Main data holder
records = []

def compare_prices(current_price, previous_price):
  try:
    percent = str((int(current_price)*100 / int(previous_price))-100).split(".")
    return percent[0]
  except:
    print(f"Something went wrong with price comparement.")
    return "UKNOWN"


def write_to_csv_file():
  with open('test.csv', 'w', newline='', encoding='utf-8') as csvfile:
    fieldnames = [
      "KONKURENCJA", 
      "DATA", 
      "MODEL", 
      "ODPOWIEDNIK",
      "NETTO",
      "BRUTTO",
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

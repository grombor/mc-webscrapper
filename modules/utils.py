#TODO: nie nadpisywanie, a dopisywanie do pliku csv

import csv

# Main data holder
records = []

def compare_prices(current_price, previous_price):
  percent = str((int(current_price)*100 / int(previous_price))-100).split(".")
  return percent[0]

def test_read_csv_file():
  with open("./modules/test.csv", newline='', encoding='UTF8') as csvfile:
    csv_reader = csv.reader(csvfile, delimiter=' ', quotechar="|")
    i=0
    for row in csv_reader:
      print(', '.join(row))
      i+=1
      if i>2:
        break

def test_write_csv_file():
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

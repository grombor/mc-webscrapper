  # TODO: if save_to_file == True : create .csv record using result dict -> create fuction that prepares that record to copy/paste
  # TODO: create function that calculate how much prices differ in %

# from .mk import print_result as Metalkas
# from .us import print_result as Umstahl
# from .lb import print_result as Locobox

import csv

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

def test_write_csv_file(rows):
  with open('eggs.csv', 'w', newline='', encoding='utf-8') as csvfile:
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

    for row in rows:
      writer.writerow(row)

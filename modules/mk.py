from bs4 import BeautifulSoup as bs4
import requests
from datetime import datetime

# List of link to scrapp
# Structure <link>, <price>, <equivalent>
links_mk = [
  ("https://sklep.metalkas.com.pl/szafy-schowkowe-metalowe-tg-4mss-eco.html", "718", "Sus 322 W"),
  ("https://sklep.metalkas.com.pl/szafa-ubraniowa-2-msu.html", "807", "Sum 320 W"),
  ("https://sklep.metalkas.com.pl/szafa-ubraniowa-3-msu-eco.html", "897", "Sum 420 W"),
  ("https://sklep.metalkas.com.pl/szafa-ubraniowa-tg-2msl-eco-basic.html", "1011", "Sul 32 W"),
  ("https://sklep.metalkas.com.pl/szafa-biurowa-1-sdb-eco.html", "1252", "Sbm 201 M"),
  ("https://sklep.metalkas.com.pl/szafa-metalowa-biurowa-tg-1sdb.html", "1450", "Sbm 202 M"),
  ("https://sklep.metalkas.com.pl/szafa-biurowa-3-sdb-eco.html", "1198", "Sbm 203 M"),
  ("https://sklep.metalkas.com.pl/szafa-kartotekowa-3-sdk.html", "2424", "Szk 301"),
  ("https://sklep.metalkas.com.pl/szafa-kartotekowa-szufladowa-tg-2sdk.html", "1888", "Szk 301"),
]

# Results: list of dict
results = []


def scrap(touple):

  # Use requests to retrieve data from a given URL
  response = requests.get(touple[0])

  # Parse the whole HTML page using BeautifulSoup
  soup = bs4(response.text, 'html.parser')

  # Parse product name
  product_name = soup.find('span', {'itemprop': 'name'}).string
  
  # Previous product price
  pprice = touple[1]

  # Current product price
  cprice = soup.find('span',{'class': 'price'}).string

  # Parse price text
  cprice = str(cprice).split(',')
  cprice = cprice[0].replace(u'\xa0', u'')

  if pprice == cprice:
    message_suffix = "\tcena nie zmieniła się\n"
  else:
    # Calculate diff in prices in precent
    percent = str(1-(int(cprice) / int(pprice))*100).split(".")
    message_suffix = f"\tróżni się od poprzednio odnotowanej ceny ({pprice} brutto) o {percent[0]}%\n"

  # Save current date
  date = datetime.now().strftime("%d/%m/%Y")
  
  # Save results of scrapping as dict
  result = {}

  # find time to ship
  t_ship = str(soup.find('div', {'class': 'single-attr unavailable'}))
  index = t_ship.find("do ")
  czas_realizacji = t_ship[index+3:-6]

  #new result
  result["KONKURENCJA"] = "Metalkas"
  result["DATA"] = date
  result["ODPOWIEDNIK"] = touple[2] + f" ( {str(product_name)} )"
  result["NETTO"] = int(int(cprice) / 1.23)
  result["BRUTTO"] = cprice
  result["WYSOKOŚĆ"] = soup.find('td', {'data-th': 'Wysokość zewnętrzna [mm]'}).string
  result["SZEROKOŚĆ"] = soup.find('td', {'data-th': 'Szerokość zewnętrzna [mm]'}).string
  result["GŁĘBOKOŚĆ"] = soup.find('td', {'data-th': 'Głębokość zewnętrzna'}).string
  result["CECHY CHARAKTERYSTYCZNE"] = soup.find('div', {'id': 'description'}).string
  result["LINK DO SKLEPU"] = touple[0]
  result["CZAS REALIZACJI"] = czas_realizacji
  result["GWARANCJA"] = "24 miesiące"
  result["msg"] = f"Metalkas: odpowiednik {result['ODPOWIEDNIK']}\n{message_suffix}"
  # TODO: add more fields from competitors database

  return results.append(result)


def scrap_all():
  for link in links_mk:
    scrap(link)


def print_result():
  scrap_all()
  for result in results:
        print(result["CZAS REALIZACJI"])
        print(result["msg"])

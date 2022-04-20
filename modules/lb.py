from bs4 import BeautifulSoup as bs4
from numpy import record
import requests
from datetime import datetime
from .utils import compare_prices, records
from .lb_links import links

# List of link to scrapp
# Structure <link>, <price>, <equivalent>
links_lb = links

# Results: list of dict
results = []

def scrap(touple):

  # Use requests to retrieve data from a given URL
  response = requests.get(touple[0])

  # Parse the whole HTML page using BeautifulSoup
  soup = bs4(response.text, 'html.parser')

  # Parse product name
  product_name = soup.find('h1', {'class': 'name'}).string.strip()
  
  # Previous product price
  pprice = touple[1]

  # Current product price
  cprice = soup.find_all('em')[1].string

  # Parse price text
  cprice = str(cprice).split(',')
  cprice = cprice[0].replace(u'\xa0', u'')

  # Save current date
  date = datetime.now().strftime("%d/%m/%Y")
  
  # Save results of scrapping as dict
  result = {}

  # find time to ship
  t_ship = str(soup.find('span', {'class': 'second'}).string)
  if t_ship == '48 - 72 H':
    index = t_ship.find("- ")
    czas_realizacji = str(int(t_ship[index+2:-2])/24).split('.')[0]
  if t_ship == '3-4 tygodnie':
    czas_realizacji = t_ship.split('-')[1]

  # czas_realizacji = ''

  if pprice == cprice:
    message = "cena nie zmieniła się.\n"
  else:
    # Calculate diff in prices in precent
    percent = compare_prices(cprice, pprice)
    message = f"cena wzrosła w stosunku do poprzednio odnotowanej ceny ({pprice} brutto) o {percent}%.\n"

    # Save current date
    date = datetime.now().strftime("%x")

  
  # Save results of scrapping as dict
    #new result
    result["KONKURENCJA"] = "Locobox"
    result["DATA"] = date
    result["MODEL"] = product_name
    result["ODPOWIEDNIK"] = touple[2]
    result["NETTO"] = cprice
    result["BRUTTO"] = int(int(cprice) * 1.23)
    result["WYSOKOŚĆ"] = 'NULL'
    result["SZEROKOŚĆ"] = 'NULL'
    result["GŁĘBOKOŚĆ"] = 'NULL'
    result["CECHY CHARAKTERYSTYCZNE"] = ""
    result["ŹRÓDŁO"] = touple[0]
    result["CZAS REALIZACJI [dni]"] = czas_realizacji
    result["GWARANCJA [miesiące]"] = "24 miesiące"
    result["msg"] = f"{result['KONKURENCJA']}: odpowiednik {result['ODPOWIEDNIK']}\n{message}"
    print(result["msg"])

    return records.append(result)


def scrap_all():
  for link in links_lb:
    scrap(link)


def get_results():
  print("Scrapping Locobox...")
  scrap_all()

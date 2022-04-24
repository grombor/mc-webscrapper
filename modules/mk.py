from bs4 import BeautifulSoup as bs4
import requests
from datetime import datetime
from .utils import compare_prices, records
from .mk_links import links

# List of link to scrapp
# Structure <link>, <price>, <equivalent>
links_mk = links


def scrap(touple):

  # Use requests to retrieve data from a given URL
  response = requests.get(touple[0])

  # Parse the whole HTML page using BeautifulSoup
  soup = bs4(response.text, 'html.parser')

  # Parse product name
  product_name = soup.find('span', {'class': 'base'}).string
  
  # Previous product price
  pprice = touple[1]

  # Current product price
  cprice = soup.find('span',{'class': 'price'})

  # Parse price text
  cprice = str(cprice).split(',')
  cprice = cprice[0].replace(u'\xa0', u'').replace('<span class="price">','')

  # Save current date
  date = datetime.now().strftime("%d/%m/%Y")
  
  # Save results of scrapping as dict
  result = {}

  # find time to ship
  t_ship = str(soup.find('div', {'class': 'single-attr unavailable'}))
  index = t_ship.find("do ")
  czas_realizacji = t_ship[index+3:-6]

  if pprice == cprice:
    message = "cena nie zmieniła się.\n"
  else:
    # Calculate diff in prices in precent
    percent = compare_prices(cprice, pprice)
    message = f"cena wzrosła w stosunku do poprzednio odnotowanej ceny ({pprice} brutto) o {percent}%.\n"

    #new result
    result["KONKURENCJA"] = "Metalkas"
    result["DATA"] = date
    result["MODEL"] = product_name
    result["ODPOWIEDNIK"] = touple[2]
    result["NETTO"] = int(int(cprice) / 1.23)
    result["BRUTTO"] = cprice
    result["WYSOKOŚĆ"] = soup.find('td', {'data-th': 'Wysokość zewnętrzna [mm]'}).string
    result["SZEROKOŚĆ"] = soup.find('td', {'data-th': 'Szerokość zewnętrzna [mm]'}).string
    result["GŁĘBOKOŚĆ"] = soup.find('td', {'data-th': 'Głębokość zewnętrzna'}).string
    result["CECHY CHARAKTERYSTYCZNE"] = ""
    result["ŹRÓDŁO"] = touple[0]
    result["CZAS REALIZACJI [dni]"] = czas_realizacji
    result["GWARANCJA [miesiące]"] = "24 miesiące"
    result["msg"] = f"Metalkas: odpowiednik {result['ODPOWIEDNIK']}\n{message}"
    print(result["msg"])


    return records.append(result)


def scrap_all():
  for link in links_mk:
    scrap(link)


def get_results():
  print("Scrapping Metalkas...")
  scrap_all()


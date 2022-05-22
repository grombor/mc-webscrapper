from bs4 import BeautifulSoup as bs4
import requests
from datetime import datetime
from .utils import compare_prices, records, wait
from .mk_links import links

# List of link to scrapp
# Structure <link>, <price>, <equivalent>
links_mk = links

def calculate_nett_price(price):
  try:
    int(int(price) / 1.23)
  except:
    return "brak danych"


def scrap(touple):

  # Use requests to retrieve data from a given URL
  response = requests.get(touple[0])

  # Parse the whole HTML page using BeautifulSoup
  soup = bs4(response.text, 'html.parser')

  # Parse product name
  product_name = soup.find('span', {'class': 'base'}).string
  
  # Previous product price
  pprice = touple[1]

  # Current product price
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

  # Cechy charakterystyczne
  try:
    cechy_charakterystyczne = soup.find("div", {"id": "description"}).find_all("li")
    temp = []
    for cecha in cechy_charakterystyczne:
      temp.append(cecha.text)
    cechy_charakterystyczne = soup.find("table", {"id": "product-attribute-specs-table"}).find_all("td")
    for cecha in cechy_charakterystyczne:
      temp.append(cecha.text)
    cechy_charakterystyczne = ' '.join(temp)
  except:
    cechy_charakterystyczne = "brak danych"

  # Comments
  if pprice == cprice:
    message = ""
  else:
    # Calculate diff in prices in precent
    percent = compare_prices(cprice, pprice)
    message = f"cena zmieniła się o {percent}."
  result["msg"] = message

  #new result
  result["DYSTRYBUTOR"] = "Metalkas"
  result["DATA"] = date
  result["MODEL"] = product_name
  result["ODPOWIEDNIK"] = touple[2]
  result["CENA KATALOGOWA NETTO"] = ""
  result["CENA SKLEPU INTERNETOWEGO NETTO"] = cprice

  result["RABAT"] = ""
  result["CENA KATALOGOWA PO RABACIE"] = ""

  try:
    result["WYSOKOŚĆ"] = soup.find('td', {'data-th': 'Wysokość zewnętrzna [mm]'}).string
    result["SZEROKOŚĆ"] = soup.find('td', {'data-th': 'Szerokość zewnętrzna [mm]'}).string
    result["GŁĘBOKOŚĆ"] = soup.find('td', {'data-th': 'Głębokość zewnętrzna'}).string
  except:
    result["WYSOKOŚĆ"] = 'UNKNOWN'
    result["SZEROKOŚĆ"] = 'UNKNOWN'
    result["GŁĘBOKOŚĆ"] = 'UNKNOWN'

  result["CECHY CHARAKTERYSTYCZNE"] = cechy_charakterystyczne
  result["ŹRÓDŁO"] = touple[0]
  result["CZAS REALIZACJI [dni]"] = czas_realizacji
  result["GWARANCJA [miesiące]"] = "24 miesiące"
  result["msg"] = message

  return records.append(result)


def scrap_all():
  for link in links_mk:
    scrap(link)
    # try:
    #   scrap(link)
    #   wait()
    # except:
    #   print(f"Something went wrong with: {link[0]}")


def get_results():
  print("Scrapping Metalkas...")
  scrap_all()


from bs4 import BeautifulSoup as bs4
import requests
from datetime import datetime
from .utils import compare_prices, records
from .km_links import links

# List of link to scrapp
# Structure <link>, <price>, <equivalent>
links_km = links


def scrap(touple):

  # Use requests to retrieve data from a given URL
  response = requests.get(touple[0])

  # Parse the whole HTML page using BeautifulSoup
  soup = bs4(response.text, 'html.parser')

  # Parse product name
  product_name = soup.find('h1', {'class': 'product_title entry-title'}).string.strip()
  
  # Previous product price
  pprice = touple[1]

  # Current product price
  cprice = soup.find_all('span', {'class': 'woocommerce-Price-amount amount'})[1]

  # Parse price text
  index1 = str(cprice).find('<bdi>')+5
  index2 = str(cprice).find(',00')
  cprice = str(cprice)[index1:index2].replace(' ','')

  # Save current date
  date = datetime.now().strftime("%d/%m/%Y")
  
  # Save results of scrapping as dict
  result = {}

  # find time to ship
  t_ship = str(soup.find_all('blockquote'))
  index1 = t_ship.find('dostawy ')+10
  index2 = t_ship.find(' tygod')
  czas_realizacji = (t_ship[index1:])[:1]
  czas_realizacji = int(czas_realizacji)*7

  if pprice == cprice:
    message = "cena nie zmieniła się.\n"
  else:
    # Calculate diff in prices in precent
    percent = compare_prices(cprice, pprice)
    message = f"cena wzrosła w stosunku do poprzednio odnotowanej ceny ({pprice} brutto) o {percent}%.\n"

    # Save current date
    date = datetime.now().strftime("%x")


    # Find dimmensions
    height = soup.find_all('td', {'width': '302'})[1].string
    width = soup.find_all('td', {'width': '302'})[3].string
    depth = soup.find_all('td', {'width': '302'})[5].string
  
  # Save results of scrapping as dict
    result["KONKURENCJA"] = "Kart-Map"
    result["DATA"] = date
    result["MODEL"] = product_name
    result["ODPOWIEDNIK"] = touple[2]
    result["NETTO"] = cprice
    result["BRUTTO"] = int(int(cprice)*1.23)
    result["WYSOKOŚĆ"] = height[:-2]
    result["SZEROKOŚĆ"] = width[:-2]
    result["GŁĘBOKOŚĆ"] = depth[:-2]
    result["CECHY CHARAKTERYSTYCZNE"] = ""
    result["ŹRÓDŁO"] = touple[0]
    result["CZAS REALIZACJI [dni]"] = czas_realizacji
    result["GWARANCJA [miesiące]"] = "24 miesiące"
    result["msg"] = f"{result['KONKURENCJA']}: odpowiednik {result['ODPOWIEDNIK']}\n{message}"
    print(result["msg"])

    return records.append(result)


def scrap_all():
  for link in links_km:
    scrap(link)


def get_results():
  print("Scrapping Kart-Map...")
  scrap_all()


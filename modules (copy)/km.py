from bs4 import BeautifulSoup as bs4
import requests
from datetime import datetime
from .utils import records, compare_prices, wait
from .km_links import links

# List of link to scrapp
links_km = links


def scrap(touple):
  result = {}

  # Use requests to retrieve data from a given URL
  response = requests.get(touple[0])

  # Parse the whole HTML page using BeautifulSoup
  soup = bs4(response.text, 'html.parser')

  # Dystrybutor
  result["DYSTRYBUTOR"] = "Kart-Map"

  # Save current date
  data = datetime.now().strftime("%d/%m/%Y")
  result["DATA"] = data

  # Parse product name
  model = soup.find('h1', {'class': 'product_title entry-title'}).string.strip()
  result["MODEL"] = model

  # Is comparable with
  result["ODPOWIEDNIK"] = touple[2]
  
  # Previous product price
  poprzednia_cena = touple[1]

  # Current product price
  netto = soup.find_all('bdi')[0].text.split(",")[0].replace(" ", "")
  result["CENA KATALOGOWA NETTO"] = ""
  result["CENA SKLEPU INTERNETOWEGO NETTO"] = netto

  result["RABAT"] = ""
  result["CENA KATALOGOWA PO RABACIE"] = ""

  # Find dimmensions
  try:
    wysokosc = soup.find_all('td', {'width': '302'})[1].string
    result["WYSOKOŚĆ"] = wysokosc[:-2]
  except:
    result["WYSOKOŚĆ"] = "brak danych"

  try:
    szerokosc = soup.find_all('td', {'width': '302'})[3].string
    result["SZEROKOŚĆ"] = szerokosc[:-2]
  except:
    result["SZEROKOŚĆ"] = "brak danych"

  try:
    glebokosc = soup.find_all('td', {'width': '302'})[5].string
    result["GŁĘBOKOŚĆ"] = glebokosc[:-2]
  except:
    result["GŁĘBOKOŚĆ"] = "brak danych"

  # Characteristics
  cechy_charakterystyczne = soup.find(id="tab-description").text
  result["CECHY CHARAKTERYSTYCZNE"] = cechy_charakterystyczne

  # Source link / cennik / katalog
  result["ŹRÓDŁO"] = touple[0]

  # Find time to ship
  czas_realziacji = soup.find_all('p', {"style":"text-align: center;"})
  result["CZAS REALIZACJI [dni]"] = czas_realziacji

  # Warranty
  result["GWARANCJA [miesiące]"] = "24 miesiące"

  # Comments
  if poprzednia_cena == netto:
    message = ""
  else:
    # Calculate diff in prices in precent
    percent = compare_prices(netto, poprzednia_cena)
    message = f"cena zmieniła się o {percent}."
  result["msg"] = message


  return records.append(result)


def scrap_all():

  for link in links_km:
    try:
      scrap(link)
      wait()
    except:
      print(f"Something went wrong with: {link[0]}")


def get_results():
  print("Scrapping Kart-Map...")
  scrap_all()


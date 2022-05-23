from bs4 import BeautifulSoup as bs4
import requests
from datetime import datetime
from .utils import records, compare_prices, wait
from .bp_links import links

# List of link to scrapp
links_km = links


def scrap(touple):
  result = {}

  # Use requests to retrieve data from a given URL
  response = requests.get(touple[0])

  # Parse the whole HTML page using BeautifulSoup
  soup = bs4(response.text, 'html.parser')

  # Dystrybutor
  result["DYSTRYBUTOR"] = "Bakpol"

  # Save current date
  data = datetime.now().strftime("%d/%m/%Y")
  result["DATA"] = data

  # Parse product name
  model = soup.find('h1', {'class': 'nazwa-produktu'}).string.strip()
  result["MODEL"] = model

  # Is comparable with
  result["ODPOWIEDNIK"] = touple[2]
  
  # Previous product price
  poprzednia_cena = touple[1]

  # Current product price
  netto = soup.find('span', {"id":"our_price_display"}).string.replace(" ", "").split(",")[0]
  # brutto = soup.find('span', {"id":"our_price_display2"}).string.replace(" ", "").split(",")[0]
  result["CENA KATALOGOWA NETTO"] = ""
  result["CENA SKLEPU INTERNETOWEGO NETTO"] = netto

  result["RABAT"] = ""
  result["CENA KATALOGOWA PO RABACIE"] = ""

  # Characteristics
  cechy_charakterystyczne = soup.find(class_="rte")
  result["CECHY CHARAKTERYSTYCZNE"] = cechy_charakterystyczne.text

  # Find dimmensions
  try:
    wysokosc = int(str(cechy_charakterystyczne.text).find('wysokość'))
    result["WYSOKOŚĆ"] = cechy_charakterystyczne.text[wysokosc+8:wysokosc+8+5+2].replace(",","").strip()
  except:
    result["WYSOKOŚĆ"] = "brak danych"

  try:
    szerokosc = int(str(cechy_charakterystyczne.text).find('szerokość'))
    result["SZEROKOŚĆ"] = cechy_charakterystyczne.text[szerokosc+9:szerokosc+9+5+2].replace(",","").strip()
  except:
    result["SZEROKOŚĆ"] = "brak danych"
    print("Problem z odczytem szerokości")

  try:
    glebokosc = int(str(cechy_charakterystyczne.text).find('głębokość'))
    result["GŁĘBOKOŚĆ"] = cechy_charakterystyczne.text[glebokosc+9:glebokosc+9+5+2].replace(",","").strip()
  except:
    result["GŁĘBOKOŚĆ"] = "brak danych"
    print("Problem z odczytem glębokości")

  # Source link / cennik / katalog
  result["ŹRÓDŁO"] = touple[0]

  # Find time to ship
  result["CZAS REALIZACJI [dni]"] = "brak danych"

  # # Warranty
  result["GWARANCJA [miesiące]"] = "24 miesiące"

  # Comments
  if poprzednia_cena == netto:
    message = ""
  else:
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
  print("Scrapping Bakpol...")
  scrap_all()


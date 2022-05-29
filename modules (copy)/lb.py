from bs4 import BeautifulSoup as bs4
import requests
from datetime import datetime
from .utils import records, compare_prices, wait
from .lb_links import links

# List of link to scrapp
links_lb = links

# Results: list of dict
results = []

def scrap(touple):

  # Use requests to retrieve data from a given URL
  # response = requests.get(touple[0])
  response = requests.get("https://www.kart-map.pl/produkt/lawka-wysuwana-podstawa-pod-szafe/")

  # Parse the whole HTML page using BeautifulSoup
  soup = bs4(response.text, 'html.parser')

  # Parse product name
  try:
    product_name = soup.find('h1', {'class': 'name'}).string.strip()
  except:
    try:
      product_name = soup.find('h1', {'class': 'product_title entry-title'}).text
    except:
      product_name = "brak danych"

  # Previous product price
  try:
    poprzednia_cena = touple[1]
  except:
    poprzednia_cena = "brak danych"
 
  # Save results of scrapping as dict
  result = {}

  # Dystrybutor
  result["DYSTRYBUTOR"] = "Locobox"

  # Save current date
  date = datetime.now().strftime("%d/%m/%Y")

  # Data
  result["DATA"] = date

  # Model
  result["MODEL"] = product_name

  # Odpowiednik
  try:
    result["ODPOWIEDNIK"] = touple[2]
  except:
    result["ODPOWIEDNIK"] = ""

  # Current product price
  try:
    netto = soup.find_all('em')[1].string
    netto = str(netto).split(',')
    netto = netto[0].replace(u'\xa0', u'')
  except:
    netto = "brak danych"

  result["CENA KATALOGOWA NETTO"] = ""
  result["CENA SKLEPU INTERNETOWEGO NETTO"] = netto

  result["RABAT"] = ""
  result["CENA KATALOGOWA PO RABACIE"] = ""

  # Dimmensions
  result["WYSOKOŚĆ"] = 'BRAK DANYCH'
  result["SZEROKOŚĆ"] = 'BRAK DANYCH'
  result["GŁĘBOKOŚĆ"] = 'BRAK DANYCH'

  # Cechy charakterystyczne
  try:
    cechy_charakterystyczne = soup.find('div', {"itemprop":'description', "class":"resetcss"}).findChildren("p")[4]
  except:
    try:
      cechy_charakterystyczne = soup.find('div', {"class":'resetcss', "itemprop":"description"}).findChildren("p")[2]
    except:
      cechy_charakterystyczne = ""
  result["CECHY CHARAKTERYSTYCZNE"] = cechy_charakterystyczne

  # Source
  result["ŹRÓDŁO"] = touple[0]

  # Gwarancja
  result["GWARANCJA [miesiące]"] = "60 miesięcy"

  # czas_realizacji
  try:
    t_ship = str(soup.find('span', {'class': 'second'}).string)
    if t_ship == '48 - 72 H':
      index = t_ship.find("- ")
      czas_realizacji = str(int(t_ship[index+2:-2])/24).split('.')[0]
    if t_ship == '3-4 tygodnie':
      czas_realizacji = t_ship.split('-')[1]
  except:
    czas_realizacji = "brak danych"

  result["CZAS REALIZACJI [dni]"] = czas_realizacji

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
  for link in links_lb:
    try:
      scrap(link)
      wait()
    except:
      print(f"Something went wrong with: {link[0]}")


def get_results():
  print("Scrapping Locobox...")
  scrap_all()

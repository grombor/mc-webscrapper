from bs4 import BeautifulSoup as bs4
from numpy import size
import requests
from datetime import datetime
from .utils import records, compare_prices, wait
from .jn_links import links

# List of link to scrapp
links_jn = links


def scrap(touple):
  result = {}

  # Use requests to retrieve data from a given URL
  response = requests.get(touple[0])

  # Parse the whole HTML page using BeautifulSoup
  soup = bs4(response.text, 'html.parser')

  # Dystrybutor
  result["DYSTRYBUTOR"] = "Jan Nowak"

  # Save current date
  data = datetime.now().strftime("%d/%m/%Y")
  result["DATA"] = data

  # Parse product name
  model = soup.find('form', {'id': 'product-cart-form'}).find('p').contents
  temp_string = str(model).replace("\\n","")
  temp_index = str(temp_string).find('Model')
  model = temp_string[temp_index+6:-2]
  result["MODEL"] = model

  # Is comparable with
  result["ODPOWIEDNIK"] = touple[2]
  
#   # Previous product price
  poprzednia_cena = touple[1]

# Current product price
  try:
    brutto = soup.find('div', {"class":"pricing"}).find('p', {"class":"current-price js-price"}).string.split(",")[0]
    brutto = str(brutto).replace(" ", "")
    netto = int(int(brutto) / 1.23)
  except:
    netto = "brak danych"
  result["CENA KATALOGOWA NETTO"] = ""
  result["CENA SKLEPU INTERNETOWEGO NETTO"] = netto

  result["RABAT"] = ""
  result["CENA KATALOGOWA PO RABACIE"] = ""

  # Characteristics
  cechy_charakterystyczne = soup.find(class_="product-desc").contents
  result["CECHY CHARAKTERYSTYCZNE"] = cechy_charakterystyczne

  # Find dimmensions
  size_box = soup.find(class_='product-sizes-panel')
  try:
    wysokosc = str(size_box.find("p", class_="normal").contents[1])[-6:-3]+"0"
    result["WYSOKOŚĆ"] = wysokosc
  except:
    result["WYSOKOŚĆ"] = "brak danych"

  try:
    szerokosc = size_box.find_all("p", class_="normal")[1].contents[1]
    result["SZEROKOŚĆ"] = szerokosc[-6:-3]+"0"
  except:
    result["SZEROKOŚĆ"] = "brak danych"
    print("Problem z odczytem szerokości")

  try:
    glebokosc = size_box.find_all("p", class_="normal")[2].contents[1]
    result["GŁĘBOKOŚĆ"] = glebokosc[-5:-3]+"0"
  except:
    result["GŁĘBOKOŚĆ"] = "brak danych"
    print("Problem z odczytem glębokości")

  # Source link / cennik / katalog
  result["ŹRÓDŁO"] = touple[0]

  # Find time to ship
  result["CZAS REALIZACJI [dni]"] = "brak danych"

  # Warranty
  result["GWARANCJA [miesiące]"] = "72 miesiące"

  # Comments
  if poprzednia_cena == netto:
    message = ""
  else:
    percent = compare_prices(netto, poprzednia_cena)
    message = f"cena zmieniła się o {percent}."
  result["msg"] = message


  return records.append(result)


def scrap_all():
  for link in links_jn:
    try:
      scrap(link)
      wait()
    except:
      print(f"Something went wrong with: {link[0]}")


def get_results():
  print("Scrapping JanNowak...")
  scrap_all()
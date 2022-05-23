from bs4 import BeautifulSoup as bs4
import requests
from datetime import datetime
from .utils import compare_prices, records, wait
from .us_links import links


links_us = links


def scrap(touple):

  result = {}

  # Use requests to retrieve data from a given URL
  response = requests.get(touple[0])

  # Parse the whole HTML page using BeautifulSoup
  soup = bs4(response.text, 'html.parser')

  # Parse product name
  product_name = soup.find('h1', {'itemprop': 'name'}).string

  # Previous product price
  pprice = touple[1]

  # Current product price
  cprice = soup.find('strong', {'id': 'net_price'}).string

  # Parse price text
  cprice = str(cprice).split('.')
  cprice = cprice[0].replace(u'\xa0', u'')

  # Save current date
  date = datetime.now().strftime("%x")

  # Find dimmensions
  try:
    temp = soup.find_all('p', {'class': 'desc-short'})[0]
    temp = str(list(temp.descendants)[2]).split('x')

    height = str(str(temp[2]).split(',')[0]+'0').replace('h','')
    width = str(temp[0]).split(',')[0]+'0'
    depth = str(temp[1]).split(',')[0]+'0'
  except:
    height = "brak danych"
    width = "brak danych"
    depth = "brak danych"
  try:
    czas_realizacji = soup.find('span', {'style': 'display: inline-block; width: 65%;'}).text
  except:
    czas_realizacji = "brak danych"

  # Cechy charakterystyczne
  temp = []
  try:
    cechy_charakterystyczne = soup.find('div', {"class": "tab-content tab1"}).find_all("li")
    for cecha in cechy_charakterystyczne:
      temp.append(cecha.text)
    cechy_charakterystyczne = ' '.join(temp)
  except:
    cechy_charakterystyczne = "brak danych"


  # Save results of scrapping as dict
  result["DYSTRYBUTOR"] = "Umstahl"
  result["DATA"] = date
  result["MODEL"] = product_name
  result["ODPOWIEDNIK"] = touple[2]
  result["CENA KATALOGOWA NETTO"] = ""
  result["CENA SKLEPU INTERNETOWEGO NETTO"] = cprice
  result["RABAT"] = ""
  result["CENA KATALOGOWA PO RABACIE"] = ""
  result["WYSOKOŚĆ"] = height
  result["SZEROKOŚĆ"] = width
  result["GŁĘBOKOŚĆ"] = depth
  result["CECHY CHARAKTERYSTYCZNE"] = cechy_charakterystyczne
  result["ŹRÓDŁO"] = touple[0]
  result["CZAS REALIZACJI [dni]"] = czas_realizacji
  result["GWARANCJA [miesiące]"] = "36 miesięcy"

  if pprice == cprice:
    message = ""
  else:
    # Calculate diff in prices in precent
    percent = compare_prices(cprice, pprice)
    message = f"cena zmieniła się o {percent}%\n"

  result["msg"] = message


  return records.append(result)


def scrap_all():
  for link in links_us:
    try:
      scrap(link)
      wait()
    except:
      print(f"Something went wrong with: {link[0]}")


def get_results():
  print("Scrapping Umstahl...")
  scrap_all()

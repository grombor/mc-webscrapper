from bs4 import BeautifulSoup as bs4
import requests
from datetime import datetime
from .utils import compare_prices, records
from .us_links import links


result = {}

links_us = links


def scrap(touple):

  # Use requests to retrieve data from a given URL
  response = requests.get(touple[0])

  # Parse the whole HTML page using BeautifulSoup
  soup = bs4(response.text, 'html.parser')

  # Parse product name
  product_name = soup.find('h1', {'itemprop': 'name'}).string
  
  # Previous product price
  pprice = touple[1]

  # Current product price
  cprice = soup.find('strong',{'id': 'net_price'}).string

  # Parse price text
  cprice = str(cprice).split('.')
  cprice = cprice[0].replace(u'\xa0', u'')

  if pprice == cprice:
    message = "cena nie zmieniła się\n"
  else:
    # Calculate diff in prices in precent
    percent = compare_prices(cprice, pprice)
    message = f"różni się od poprzednio odnotowanej ceny ({pprice} brutto) o {percent}%\n"

    # Save current date
    date = datetime.now().strftime("%x")

    # Find dimmensions
    temp = soup.find_all('p', {'class': 'desc-short'})[0]
    temp = str(list(temp.descendants)[2]).split('x')
    
    height = str(str(temp[2]).split(',')[0]+'0').replace('h','')
    width = str(temp[0]).split(',')[0]+'0'
    depth = str(temp[1]).split(',')[0]+'0'
    czas_realizacji = soup.find('span', {'style': 'display: inline-block; width: 65%;'}).string

  
    # Save results of scrapping as dict
    result["KONKURENCJA"] = "Umstahl"
    result["DATA"] = date
    result["MODEL"] = product_name
    result["ODPOWIEDNIK"] = touple[2]
    result["NETTO"] = cprice
    result["BRUTTO"] = int(int(cprice)*1.23)
    result["WYSOKOŚĆ"] = height
    result["SZEROKOŚĆ"] = width
    result["GŁĘBOKOŚĆ"] = depth
    result["CECHY CHARAKTERYSTYCZNE"] = ""
    result["ŹRÓDŁO"] = touple[0]
    result["CZAS REALIZACJI [dni]"] = czas_realizacji
    result["GWARANCJA [miesiące]"] = "36 miesięcy"
    result["msg"] = f"{result['KONKURENCJA']}: odpowiednik {result['ODPOWIEDNIK']}\n{message}"
    print(result["msg"])

  return records.append(result)


def scrap_all():
  for link in links_us:
    scrap(link)


def get_results():
  print("Scrapping Umstahl...")
  scrap_all()

from bs4 import BeautifulSoup as bs4
import requests
from datetime import datetime

# List of link to scrapp
# Structure <link>, <price>, <equivalent>
links = [
  ("https://sklep.metalkas.com.pl/szafa-ubraniowa-2-msu-eco-mtd.html", "500", "Sum 320 W"),
  ("https://sklep.metalkas.com.pl/tg-5msu-eco.html", "600", "Sus 333 W"),
]

# Results: list of dict
results = []

# Message text
message = "Metalkas: cena odpowiednika Sum 320 W "


def scrap(touple):

  # Use requests to retrieve data from a given URL
  response = requests.get(touple[0])

  # Parse the whole HTML page using BeautifulSoup
  soup = bs4(response.text, 'html.parser')

  # Parse product name
  product_name = soup.find('span', {'itemprop': 'name'}).string
  
  # Previous product price
  pprice = touple[1]

  # Current product price
  cprice = soup.find('span',{'class': 'price'}).string

  # Parse price text
  cprice = str(cprice).split(',')
  cprice = cprice[0].replace(u'\xa0', u'')

  if pprice == cprice:
    message_suffix = "\tcena nie zmieniła się"
  else:
    # Calculate diff in prices in precent
    percent = str((int(cprice) / int(pprice))*100).split(".")
    message_suffix = f"\tróżni się od poprzednio odnotowanej ceny ({pprice} brutto) o {percent[0]}%\n"

  # Save current date
  date = datetime.now().strftime("%x")
  
  # Save results of scrapping as dict
  result = {}
  result["link"] = touple[0]
  result["odpowiednik"] = touple[2] + f" ( {str(product_name)} )"
  result["cena"] = cprice
  result["data"] = date
  result["msg"] = f"Metalkas: odpowiednik {result['odpowiednik']}\n{message_suffix}"
  # TODO: add more fields from competitors database

  return results.append(result)


def scrapp_all():
  for link in links:
    scrap(link)


def print_result():
  scrapp_all()
  #print(results)
  for result in results:
        print(result["msg"])

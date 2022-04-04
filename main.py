from bs4 import BeautifulSoup as bs4
import requests
from datetime import datetime

# variables
results = []
links = []

# functions for all sections
def scrap_mk(touple):
    
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
    message_suffix = ""
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

def scrapp_all_links_mk(links):
    for link in links:
        scrap_mk(link)


# List of Metalkas links to scrapp.
# structure: <link> <price> <equivalent model>
links_mk = [
  ("https://sklep.metalkas.com.pl/szafa-ubraniowa-2-msu-eco-mtd.html", "500", "Sum 320 W"),
  ("https://sklep.metalkas.com.pl/tg-5msu-eco.html", "600", "Sus 333 W"),
]


def print_result():
  scrapp_all_links_mk()
  for result in results:
        print(result["msg"])

   
# List of Metalkas links to scrapp.
# structure: <link> <price> <equivalent model>
links_us = [
  ("https://umstahl.pl/metalowa-szafka-ubraniowa-se-30r2-24h,id102.html", "500", "Sum 320 W"),
 ("https://umstahl.pl/metalowa-szafa-ubraniowa-sle-40r2-24h,id104.html", "1024", "Sus 333 W"),
]

# Message text
message = "Umstahl: cena odpowiednika Sum 320 W "


def scrap_us(touple):

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
  result["msg"] = f"Umstahl: odpowiednik {result['odpowiednik']}\n{message_suffix}"
  # TODO: add more fields from competitors database

  return results.append(result)


def scrapp_all_links_us(links):
  for link in links:
    scrap_us(link)


def print_result():
  for result in results:
        print(result["msg"])



scrapp_all_links_mk(links_mk)
scrapp_all_links_us(links_us)
print_result()






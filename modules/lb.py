from bs4 import BeautifulSoup as bs4
import requests
from datetime import datetime

# List of link to scrapp
# Structure <link>, <price>, <equivalent>
links = [
  ("https://locobox.pl/pl/p/Szafka-szkolna-dla-4-uczniow-4D-s60-cm%2C-h180-cm/257", "628", "Sus 322 W"),
  ("https://locobox.pl/pl/p/Szafa-ubraniowa-PROFI-U2-s60-cm/284", "449", "Sum 320 W"),
  ("https://locobox.pl/pl/p/Szafa-ubraniowa-PROFI-U2-s80-cm/288", "583", "Sum 420 W"),
  ("https://locobox.pl/pl/p/Szafa-ubraniowa-PROFI-L4-s60-cm/323", "1013", "Sul 32 W"),
  ("https://locobox.pl/pl/p/Szafa-aktowa-PROFI-O80200-RODO/545", "855", "Sbm 202 M"),
  ("https://locobox.pl/pl/p/Szafa-aktowa-PROFI-O80200-RODO/545", "905", "Sbm 203 M"),
  ("https://locobox.pl/pl/p/Szafa-kartotekowa-PROFI-F4xA4/1028", "775", "Szk 301"),
]

# Results: list of dict
results = []

def scrap(touple):

  # Use requests to retrieve data from a given URL
  response = requests.get(touple[0])

  # Parse the whole HTML page using BeautifulSoup
  soup = bs4(response.text, 'html.parser')

  # Parse product name
  product_name = soup.find('h1', {'class': 'name'}).string.strip()
  
  # Previous product price
  pprice = touple[1]

  # Current product price
  cprice = soup.find_all('em')[1].string

  # Parse price text
  cprice = str(cprice).split(',')
  cprice = cprice[0].replace(u'\xa0', u'')

  if pprice == cprice:
    message_suffix = "\tcena nie zmieniła się\n"
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
  result["msg"] = f"Locobox: odpowiednik {result['odpowiednik']}\n{message_suffix}"
  # TODO: add more fields from competitors database

  return results.append(result)


def scrapp_all():
    for link in links:
        scrap(link)


def print_result():
  scrapp_all()
  for result in results:
        print(result["msg"])

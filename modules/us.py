from bs4 import BeautifulSoup as bs4
import requests
from datetime import datetime

# List of link to scrapp
# Structure <link>, <price>, <equivalent>
links = [
 ("https://umstahl.pl/metalowa-szafa-ubraniowa-sle-30r2,id403.html", "1102", "Sul 32 W"),
 ("https://umstahl.pl/metalowa-szafa-ubraniowa-z-podzialem-wewnetrznym-se-40r2-24h,id550.html", "721", "Sum 420 W"),
 ("https://umstahl.pl/metalowa-szafka-ubraniowa-se-30r2-24h,id102.html", "459", "Sum 320 W"),
 ("https://umstahl.pl/metalowa-szafa-kartotekowa-a4-4ra4-24h,id540.html", "983", "Szk 301"),
 ("https://umstahl.pl/szafa-metalowa-aktowa-m-1ola-500,id199.html", "907", "Sbm 201 M"),
 ("https://umstahl.pl/szafa-metalowa-aktowa-m-2ola-1000,id53.html", "1037", "Sbm 203 M"),
]

# Results: list of dict
results = []


# Message text
message = "Umstahl: cena odpowiednika Sum 320 W "


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
  result["msg"] = f"Umstahl: odpowiednik {result['odpowiednik']}\n{message_suffix}"
  # TODO: add more fields from competitors database

  return results.append(result)


def scrapp_all():
  for link in links:
    scrap(link)


def print_result():
  scrapp_all()
  for result in results:
        print(result["msg"])

from bs4 import BeautifulSoup as bs4
import requests
from datetime import datetime

# variables
results = []
links = []



# List of Metalkas links to scrapp.
# structure: <link> <price> <equivalent model>
links_mk = [
  ("https://sklep.metalkas.com.pl/szafy-schowkowe-metalowe-tg-4mss-eco.html", "718", "Sus 322 W"),
  ("https://sklep.metalkas.com.pl/szafa-ubraniowa-2-msu.html", "807", "Sum 320 W"),
  ("https://sklep.metalkas.com.pl/szafa-ubraniowa-3-msu-eco.html", "897", "Sum 420 W"),
  ("https://sklep.metalkas.com.pl/szafa-ubraniowa-tg-2msl-eco-basic.html", "1011", "Sul 32 W"),
  ("https://sklep.metalkas.com.pl/szafa-biurowa-1-sdb-eco.html", "1252", "Sbm 201 M"),
  ("https://sklep.metalkas.com.pl/szafa-biurowa-3-sdb-eco.html", "1198", "Sbm 203 M"),
  ("https://sklep.metalkas.com.pl/szafa-kartotekowa-3-sdk.html", "2424", "Szk 301"),
  ("https://sklep.metalkas.com.pl/szafa-kartotekowa-szufladowa-tg-2sdk.html", "1888", "Szk 301"),
]

# functions for Metalkas
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
  result["msg"] = f"Metalkas: odpowiednik {result['odpowiednik']}\n{message_suffix}"
  # TODO: add more fields from competitors database

  return results.append(result)


def scrapp_all_links_mk(links):
    for link in links:
        scrap_mk(link)

   
# List of Umstahl links to scrapp.
# structure: <link> <price> <equivalent model>
links_us = [
 ("https://umstahl.pl/metalowa-szafa-ubraniowa-sle-30r2,id403.html", "1102", "Sul 32 W"),
 ("https://umstahl.pl/metalowa-szafa-ubraniowa-z-podzialem-wewnetrznym-se-40r2-24h,id550.html", "721", "Sum 420 W"),
 ("https://umstahl.pl/metalowa-szafka-ubraniowa-se-30r2-24h,id102.html", "459", "Sum 320 W"),
 ("https://umstahl.pl/metalowa-szafa-kartotekowa-a4-4ra4-24h,id540.html", "983", "Szk 301"),
 ("https://umstahl.pl/szafa-metalowa-aktowa-m-1ola-500,id199.html", "907", "Sbm 201 M"),
 ("https://umstahl.pl/szafa-metalowa-aktowa-m-2ola-1000,id53.html", "1037", "Sbm 203 M"),
]

# functions for Umstahl
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


def scrapp_all_links_us(links):
  for link in links:
    scrap_us(link)



# List of Locobox links to scrapp.
# structure: <link> <price> <equivalent model>
links_lb = [
  ("https://locobox.pl/pl/p/Szafka-szkolna-dla-4-uczniow-4D-s60-cm%2C-h180-cm/257", "628", "Sus 322 W"),
  ("https://locobox.pl/pl/p/Szafa-ubraniowa-PROFI-U2-s60-cm/284", "449", "Sum 320 W"),
  ("https://locobox.pl/pl/p/Szafa-ubraniowa-PROFI-U2-s80-cm/288", "583", "Sum 420 W"),
  ("https://locobox.pl/pl/p/Szafa-ubraniowa-PROFI-L4-s60-cm/323", "1013", "Sul 32 W"),
  ("https://locobox.pl/pl/p/Szafa-aktowa-PROFI-O80200-RODO/545", "855", "Sbm 202 M"),
  ("https://locobox.pl/pl/p/Szafa-aktowa-PROFI-O80200-RODO/545", "905", "Sbm 203 M"),
  ("https://locobox.pl/pl/p/Szafa-kartotekowa-PROFI-F4xA4/1028", "775", "Szk 301"),
]


# functions for Locobox
def scrap_lb(touple):

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


def scrapp_all_links_lb(links):
  for link in links:
    scrap_lb(link)



def print_result():
  for result in results:
        print(result["msg"])



scrapp_all_links_mk(links_mk)
scrapp_all_links_us(links_us)
scrapp_all_links_lb(links_lb)
print_result()






from bs4 import BeautifulSoup as bs4
import requests

# List of link to scrapp
links = [
  "https://sklep.metalkas.com.pl/szafa-ubraniowa-2-msu-eco-mtd.html"
]

# List of results
results = []

# Message text
message = "Metalkas: cena odpowiednika Sum 320 W "

# Metalkas's product URL
#url = 'https://sklep.metalkas.com.pl/szafa-ubraniowa-2-msu-eco-mtd.html'

def scrap(url):

  # Use requests to retrieve data from a given URL
  response = requests.get(url)

  # Parse the whole HTML page using BeautifulSoup
  soup = bs4(response.text, 'html.parser')

  # Parse product name
  product_name = soup.find('span', {'itemprop': 'name'}).string
  
  # Previous product price
  pprice = '605'

  # Current product price
  cprice = soup.find('span',{'class': 'price'}).string

  # Parse price text
  cprice = str(cprice).split(',')

  if pprice == cprice[0]:
    message2 = " nie różni się od poprzedniej ceny."
  else:
    message2 = f" różni się od poprzedniej ceny ({pprice} brutto)"

  return results.append(message + str(product_name) + message2)


def scrapp_all():
  for link in links:
    scrap(link)


def print_result():
  scrapp_all()
  print(results)
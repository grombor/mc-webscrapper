from bs4 import BeautifulSoup as bs4
import requests
from src.mc_webscrapper.bakpol_links import links
from src.mc_webscrapper.utils import get_date, Error, compare_prices, records


class Bakpol:
    """ This class represents products of Bakpol manufacturer (https://bakpol.pl/)"""


    def get_links(self) -> list:
        """ Import links from a file."""
        try:
            if len(links) <= 0:
                raise Error("Links list is empty or broken.")
            return links
        except Error as ve:
            print(ve)


    def get_model(self, url, soup) -> str:
        """ Get product model. """
        try:
            model = soup.find('h1', {'class': 'nazwa-produktu'}).string.strip()
            return model
            raise Error(f"Something wrong with product name in {url}.")
        except Error as ve:
            print(ve)
            model = ""


    def get_price(self, url, soup):
        """ Get product price. """
        try:
            return soup.find('span', {"id": "our_price_display"}).string.replace(" ", "").split(",")[0]
            raise Error(f"Something wrong with product price in {url}.")
        except Error as ve:
            print(ve)
            return f""


    def get_height(self, url, soup) -> str:
        """ Get product height. """
        try:
            cechy_charakterystyczne = soup.find(class_="rte")
            wysokosc = int(str(cechy_charakterystyczne.text).find('wysokość'))
            return cechy_charakterystyczne.text[wysokosc+8:wysokosc+8+5+2].replace(",", "").strip()
            raise Error(f"Something wrong with height in {url}.")
        except Error as ve:
            print(ve)
            return f""


    def get_width(self, url, soup) -> str:
        """ Get product width. """
        try:
            cechy_charakterystyczne = soup.find(class_="rte")
            szerokosc = int(str(cechy_charakterystyczne.text).find('szerokość'))
            return cechy_charakterystyczne.text[szerokosc + 9:szerokosc + 9 + 5 + 2].replace(",","").strip()
            raise Error(f"Something wrong with width in {url}.")
        except Error as ve:
            print(ve)
            return f""


    def get_depth(self, url, soup) -> str:
        """ Get product depth. """
        try:
            cechy_charakterystyczne = soup.find(class_="rte")
            glebokosc = int(str(cechy_charakterystyczne.text).find('głębokość'))
            return cechy_charakterystyczne.text[glebokosc + 9:glebokosc + 9 + 5 + 2].replace(",","").strip()
            raise Error(f"Something wrong with depth in {url}.")
        except Error as ve:
            print(ve)
            return f""


    def get_description(self, url, soup) -> str:
        """ Get product description. """
        try:
            cechy_charakterystyczne = soup.find(class_="rte").text
            return cechy_charakterystyczne
            raise Error(f"Something wrong with description in {url}.")
        except Error as ve:
            print(ve)
            return f""


    def get_comment(self, previous_price, nett) -> str:
        """ Create product comment. """
        try:
            if previous_price == nett:
                return ""
            else:
                return compare_prices(nett, previous_price)
            raise Error(f"Something wrong with comment in {url}.")
        except Error as ve:
            print(ve)
            return f""


    def scrap_link(self, link):
        """ Scraps given url, gathers all data and create dictionary record. """

        result = dict()

        # Save current dealer
        result["DYSTRYBUTOR"] = "Bakpol"

        # Save current date
        result["DATA"] = get_date()

        # Use requests to retrieve data from a given URL
        url = link[0]
        response = requests.get(url)

        # Parse the whole HTML page using BeautifulSoup
        soup = bs4(response.text, 'html.parser')

        # Parse product name
        result["MODEL"] = self.get_model(url, soup)

        # Is comparable with
        result["ODPOWIEDNIK"] = link[2]

        # If position is not from price list of catalogue - leave it empty
        result["CENA KATALOGOWA NETTO"] = ""

        # Current product price
        result["CENA SKLEPU INTERNETOWEGO NETTO"] = self.get_price(url, soup)

        # If position is not from price list of catalogue - leave it empty
        result["RABAT"] = ""
        result["CENA KATALOGOWA PO RABACIE"] = ""

        # Find dimmensions
        result["WYSOKOŚĆ"] = self.get_height(url, soup)
        result["SZEROKOŚĆ"] = self.get_width(url, soup)
        result["GŁĘBOKOŚĆ"] = self.get_depth(url, soup)

        # Characteristics
        result["CECHY CHARAKTERYSTYCZNE"] = self.get_description(url, soup)

        # Source url / price list / catalogue
        result["ŹRÓDŁO"] = url

        # Find shipping time
        result["CZAS REALIZACJI [dni]"] = ""

        # Warranty
        result["GWARANCJA [miesiące]"] = "24 miesiące"

        # Comment
        if result["CENA SKLEPU INTERNETOWEGO NETTO"] != "":
            result["msg"] = self.get_comment(link[1], result["CENA SKLEPU INTERNETOWEGO NETTO"])
        else:
            result["msg"] = ""

        return records.append(result)

    def scrap(self):
        """Scrap through all links in a list."""

        print("Starting scrapping Bakpol.")
        for link in links:
            try:
                self.scrap_link(link)
                return "Done."
                raise Error(link[0])
            except Error as e:
                print(e)


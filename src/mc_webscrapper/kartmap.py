from bs4 import BeautifulSoup as bs4
import requests
from src.mc_webscrapper.kartmap_links import links
from src.mc_webscrapper.utils import get_date, compare_prices, records
from src.mc_webscrapper.errors import Error


class KartMap:
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
            return soup.find('h1', {'class': 'product_title entry-title'}).string.strip()
            raise Error(f"Something wrong with product name in {url}.")
        except Error as ve:
            print(ve)
            return ""


    def get_price(self, url, soup):
        """ Get product price. """
        try:
            return soup.find_all('bdi')[0].text.split(",")[0].replace(" ", "")
            raise Error(f"Something wrong with product price in {url}.")
        except (Error, IndexError) as ve:
            print(ve)
            return ""
        # except (Error, IndexError) as ve:
        #     print(ve)
        #     return ""


    def get_height(self, url, soup) -> str:
        """ Get product height. """
        try:
            height = soup.find_all('td', {'width': '302'})[1].text[:-2]
            return height
            raise Error(f"Something wrong with height in {url}.")
        except (Error, IndexError) as ve:
            print(ve)
            return f""


    def get_width(self, url, soup) -> str:
        """ Get product width. """
        try:
            szerokosc = soup.find_all('td', {'width': '302'})[3].string
            return szerokosc[:-2]
            raise Error(f"Something wrong with width in {url}.")
        except (Error, IndexError) as ve:
            print(ve)
            return f""


    def get_depth(self, url, soup) -> str:
        """ Get product depth. """
        try:
            return soup.find_all('td', {'width': '302'})[5].string
            raise Error(f"Something wrong with depth in {url}.")
        except (Error, IndexError) as ve:
            print(ve)
            return f""


    def get_description(self, url, soup) -> str:
        """ Get product description. """
        try:
            return soup.find(id="tab-description").text
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
        result["DYSTRYBUTOR"] = "Kart-Map"

        # Save current date
        result["DATA"] = get_date()

        # Use requests to retrieve data from a given URL
        url = link[0]
        headers = requests.utils.default_headers()
        headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        })
        response = requests.get(url, headers=headers)

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
        result["CZAS REALIZACJI [dni]"] = soup.find_all('p', {"style":"text-align: center;"})

        # Warranty
        result["GWARANCJA [miesiące]"] = "24 miesiące"

        # Comment
        if type(result["CENA SKLEPU INTERNETOWEGO NETTO"]) == int:
            result["msg"] = self.get_comment(link[1], result["CENA SKLEPU INTERNETOWEGO NETTO"])
        else:
            result["msg"] = ""

        return records.append(result)

    def scrap(self):
        """Scrap through all links in a list."""

        print("Starting scrapping Kartmap.")
        for link in links:
            try:
                self.scrap_link(link)
            except Error as e:
                print(e, f"Something wrong with {link[0]}")


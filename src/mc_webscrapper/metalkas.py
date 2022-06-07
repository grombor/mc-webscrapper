from bs4 import BeautifulSoup as bs4
import requests
from src.mc_webscrapper.metalkas_links import links
from src.mc_webscrapper.utils import get_date, compare_prices, records, requests_timeout, show_status, extract_digits
from src.mc_webscrapper.errors import Error


class Metalkas:
    """ This class represents products of Metalkas manufacturer (https://bakpol.pl/)"""


    def calculate_nett_price(price):
        try:
            int(int(price) / 1.23)
        except Error as er:
            print(er)
            return ""

    def get_links(self) -> list:
        """ Import links from a file."""
        try:
            if len(links) <= 0:
                raise Error("Links list is empty or broken.")
            return links
        except Error as e:
            print(e)


    def get_model(self, url, soup) -> str:
        """ Get product model. """
        try:
            return soup.find('span', {'class': 'base'}).string
        except ValueError as e:
            print(e, f", method: {self.get_model.__name__} link: {url}")
            return ""


    def get_price(self, url, soup):
        """ Get product price. """
        try:
            price = soup.find('span', {'class': 'price'})
            price = str(price).split(',')[0]
            if type(price) != None:
                return extract_digits(price)
            else:
                raise Error
        except Error as e:
            print(e, f", method: {self.get_price.__name__} link: {url}")
            return ""


    def get_height(self, url, soup) -> str:
        """ Get product height. """
        try:
            height = soup.find('td', {'data-th': 'Wysokość zewnętrzna [mm]'}).text
            return extract_digits(height)
        except (AttributeError, ValueError) as e:
            print(e, f", method: {self.get_height.__name__} link: {url}")
            return ""


    def get_width(self, url, soup) -> str:
        """ Get product width. """
        try:
            width = soup.find('td', {'data-th': 'Szerokość zewnętrzna [mm]'}).text
            return extract_digits(width)
        except (AttributeError, ValueError) as e:
            print(e, f", method: {self.get_width.__name__} link: {url}")
            return ""


    def get_depth(self, url, soup) -> str:
        """ Get product depth. """
        try:
            depth = soup.find('td', {'data-th': 'Głębokość zewnętrzna'}).text
            return extract_digits(depth)
        except (AttributeError, ValueError, IndexError) as e:
            print(e, f", method: {self.get_depth.__name__} link: {url}")
            return ""


    def get_description(self, url, soup) -> str:
        """ Get product description. """
        try:
            try:
                cechy_charakterystyczne = soup.find("div", {"id": "description"}).find_all("li")
                temp = []
                for cecha in cechy_charakterystyczne:
                    temp.append(cecha.text)
                cechy_charakterystyczne = soup.find("table", {"id": "product-attribute-specs-table"}).find_all("td")
                for cecha in cechy_charakterystyczne:
                    temp.append(cecha.text)
                cechy_charakterystyczne = ' '.join(temp)
                return cechy_charakterystyczne
            except (AttributeError, IndexError):
                return soup.find('div', {"class": 'resetcss', "itemprop": "description"}).findChildren("p")[2]
        except (AttributeError, ValueError) as e:
            print(e, f", method: {self.get_description.__name__} link: {url}")
            return ""


    def get_shipping_time(self, url, soup):
        """ Get product shipping time. """
        try:
            return soup.find('td', {'data-th': 'Czas realizacji'}).text
        except (AttributeError, ValueError, IndexError) as e:
            print(e, f", method: {self.get_depth.__name__} link: {url}")
            return ""


    def get_comment(self, previous_price, nett) -> str:
        """ Create product comment. """
        try:
            if previous_price == nett:
                return ""
            else:
                return compare_prices(nett, previous_price)
            raise Error(f"Something wrong with comment in {url}.")
        except (ValueError, IndexError) as e:
            print(e, f", method: {self.get_depth.__name__} link: {url}")
            return ""


    def scrap_link(self, link):
        """ Scraps given url, gathers all data and create dictionary record. """

        result = dict()

        # Save current dealer
        result["DYSTRYBUTOR"] = "Metalkas"

        # Save current date
        result["DATA"] = get_date()

        # Use requests to retrieve data from a given URL
        url = link[0]
        headers = requests.utils.default_headers()
        headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
        })
        response = requests.get(url, timeout=requests_timeout, headers=headers)

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
        result["CZAS REALIZACJI [dni]"] = self.get_shipping_time(url, soup)

        # Warranty
        result["GWARANCJA [miesiące]"] = "2"

        # Comment
        if result["CENA SKLEPU INTERNETOWEGO NETTO"] != "":
            result["msg"] = self.get_comment(link[1], result["CENA SKLEPU INTERNETOWEGO NETTO"])
        else:
            result["msg"] = ""

        return records.append(result)

    def scrap(self):
        """Scrap through all links in a list."""

        print("Starting scrapping Metalkas.")
        i = 0
        for link in links:
            try:
                i += 1
                show_status(i, links)
                self.scrap_link(link)
            except Error as e:
                print(e, f"Something wrong with {link[0]}")


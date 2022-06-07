from bs4 import BeautifulSoup as bs4
import requests
from src.mc_webscrapper.kartmap_links import links
from src.mc_webscrapper.utils import get_date, compare_prices, records, requests_timeout, extract_digits, show_status
from src.mc_webscrapper.errors import Error


class KartMap:
    """ This class represents products of Bakpol manufacturer (https://bakpol.pl/)"""


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
            return soup.find('h1', {'class': 'product_title entry-title'}).text
        except (AttributeError, ValueError) as e:
            print(e, f", method: {self.get_model.__name__} link: {url}")
            return ""


    def get_price(self, url, soup):
        """ Get product price. """
        try:
            price = soup.find("span", class_="price").text
            if type(price) != None:
                return price.replace(" ", "").split(",")[0]
            else:
                raise Error
        except Error as e:
            print(e, f", method: {self.get_price.__name__} link: {url}")
            return ""



    def get_height(self, url, soup) -> str:
        """ Get product height. """
        try:
            height = soup.find_all('td', {'width': '302'})[1].text
            return extract_digits(height)
        except (ValueError, IndexError, AttributeError) as e:
            print(e)
            return f""


    def get_width(self, url, soup) -> str:
        """ Get product width. """
        try:
            szerokosc = soup.find_all('td', {'width': '302'})[3].string
            return extract_digits(szerokosc)
        except (ValueError, IndexError, AttributeError) as e:
            print(e)
            return f""


    def get_depth(self, url, soup) -> str:
        """ Get product depth. """
        try:
            depth = soup.find_all('td', {'width': '302'})[5].text
            return extract_digits(depth)
        except (ValueError, IndexError, AttributeError) as e:
            print(e)
            return f""


    def get_description(self, url, soup) -> str:
        """ Get product description. """
        try:
            return soup.find(id="tab-description").text
        except (IndexError, AttributeError) as e:
            print(url)
            return f""


    def get_status(self, url, soup):
        """ Get shipping status. """
        try:
            return soup.find('p', {"style":"text-align: center;"}).text
        except (IndexError, AttributeError) as e:
            print(url)
            return f""



    def get_comment(self, previous_price, nett) -> str:
        """ Create product comment. """
        try:
            if previous_price == nett:
                return ""
            else:
                return compare_prices(nett, previous_price)
        except AttributeError as ve:
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
        result["CZAS REALIZACJI [dni]"] = self.get_status(url, soup)

        # Warranty
        result["GWARANCJA [miesiące]"] = "2 lata"

        # Comment
        if type(result["CENA SKLEPU INTERNETOWEGO NETTO"]) == int:
            result["msg"] = self.get_comment(link[1], result["CENA SKLEPU INTERNETOWEGO NETTO"])
        else:
            result["msg"] = ""

        return records.append(result)

    def scrap(self):
        """Scrap through all links in a list."""

        print("Starting scrapping Kartmap.")
        i = 0
        for link in links:
            try:
                i += 1
                show_status(i, links)
                self.scrap_link(link)
            except Error as e:
                print(e, f"Something wrong with {link[0]}")


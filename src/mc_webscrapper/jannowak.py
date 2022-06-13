from bs4 import BeautifulSoup as bs4
import requests
from src.mc_webscrapper.jannowak_links import links
from src.mc_webscrapper.utils import get_date, compare_prices, records, show_status, requests_timeout, extract_digits
from src.mc_webscrapper.errors import Error


class JanNowak:
    """ This class represents products of Jan Nowak manufacturer & dealer (https://jannowak.com/)"""


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
            model = soup.find('form', {'id': 'product-cart-form'}).find('p').contents
            temp_string = str(model).replace("\\n", "")
            temp_index = str(temp_string).find('Model')
            model = temp_string[temp_index + 6:-2]
            return model
            raise Error(f"Something wrong with product name in {url}.")
        except ValueError as e:
            print(e, f", method: {self.get_model.__name__} link: {url}")
            return ""


    def get_price(self, url, soup):
        """ Get product price. """
        try:
            brutto = soup.find('div', {"class": "pricing"}).find('p', {"class": "current-price js-price"}).string.replace(" ", "").split(",")[0]
            brutto = extract_digits(brutto)
            return int(int(brutto)/1.23)
        except AttributeError as e:
            try:
                brutto = soup.find('div', {"class": "pricing"}).find('p', {"class": "current-price js-price"}).text.split(",")[0]
                brutto = extract_digits(brutto)
                return int(int(brutto) / 1.23)
            except AttributeError as e:
                print(e, f", method: {self.get_price.__name__} link: {url}")
                return ""


    def get_height(self, url, soup) -> str:
        """ Get product height. """
        try:
            height = soup.find_all("p", class_="normal")[0].text[:-2]
            height = extract_digits(height)
            return height+"0"
        except (AttributeError, TypeError, ValueError) as e:
            print(e, f", method: {self.get_height.__name__} link: {url}")
            return ""


    def get_width(self, url, soup) -> str:
        """ Get product width. """
        try:
            width = soup.find_all("p", class_="normal")[1].text[:-2]
            width = extract_digits(width)
            return width+"0"
        except (ValueError, AttributeError, TypeError) as e:
            print(e, f", method: {self.get_width.__name__} link: {url}")
            return ""


    def get_depth(self, url, soup) -> str:
        """ Get product depth. """
        try:
            depth = soup.find_all("p", class_="normal")[2].text[:-2]
            depth = extract_digits(depth)
            return depth+"0"
        except (ValueError, IndexError, AttributeError, TypeError) as e:
            print(e, f", method: {self.get_depth.__name__} link: {url}")
            return ""


    def get_description(self, url, soup) -> str:
        """ Get product description. """
        try:
            return soup.find(class_="product-desc").text[1:]
        except (ValueError, IndexError, AttributeError) as e:
            print(e, f", method: {self.get_description.__name__} link: {url}")
            return ""


    def get_status(self, url, soup):
        """ Get shipping status. """
        try:
            return soup.find("p", class_="status").text
        except (ValueError, IndexError, AttributeError) as e:
            print(e, f", method: {self.get_description.__name__} link: {url}")
            return ""


    def get_comment(self, previous_price, nett, url) -> str:
        """ Create product comment. """
        try:
            if previous_price == nett:
                return ""
            else:
                return compare_prices(nett, previous_price)
        except (ValueError, IndexError) as e:
            print(e, f", method: {self.get_depth.__name__} link: {url}")
            return ""


    def scrap_link(self, link):
        """ Scraps given url, gathers all data and create dictionary record. """

        result = dict()

        # Save current dealer
        result["DYSTRYBUTOR"] = "Jan Nowak"

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
        result["GWARANCJA [miesiące]"] = "6"

        # Comment
        if result["CENA SKLEPU INTERNETOWEGO NETTO"] != "":
            result["msg"] = self.get_comment(link[1], result["CENA SKLEPU INTERNETOWEGO NETTO"], url)
        else:
            result["msg"] = ""

        return records.append(result)


    def scrap(self):
        """Scrap through all links in a list."""

        print("Starting scrapping Jan Nowak.")
        i = 0
        for link in links:
            try:
                i += 1
                show_status(i, links)
                self.scrap_link(link)
            except Error as e:
                print(e, f"Something wrong with {link[0]}")


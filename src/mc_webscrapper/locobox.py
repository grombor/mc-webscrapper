from bs4 import BeautifulSoup as bs4
import requests
from src.mc_webscrapper.locobox_links import links
from src.mc_webscrapper.utils import get_date, compare_prices, records, requests_timeout, extract_digits, show_status
from src.mc_webscrapper.errors import Error


class Locobox:
    """ This class represents products of Bakpol manufacturer (https://locobox.pl/)"""


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
            return soup.find('h1', {'class': 'name'}).string.strip()
        except (AttributeError, ValueError) as e:
            print(e, f", method: {self.get_model.__name__} link: {url}")
            return ""


    def get_price(self, url, soup):
        """ Get product price. """
        try:
            netto = soup.find_all('em')[1].string
            netto = str(netto).split(',')
            return extract_digits(netto[0])
            raise Error(f"Something wrong with product price in {url}.")
        except Error as e:
            print(e, f", method: {self.get_price.__name__} link: {url}")
            return ""



    def get_height(self, url, soup) -> str:
        """ Get product height. """
        try:
            height = soup.find_all('td', {'width': '302'})[1].text
            return extract_digits(height)
        except IndexError as e:
            try:
                temp = soup.find('div', {'itemprop': 'description'}).contents[4].text.split(": ")[1]
                height = str(temp)[:3]+"0"
                return height
            except (AttributeError, IndexError):
                try:
                    temp = soup.find('div', {'itemprop': 'description'}).contents[6].text.split(": ")[1]
                    height = str(temp)[:3]+"0"
                    return (height)
                except (AttributeError, ValueError, IndexError):
                    return ""
        except (AttributeError, ValueError) as e:
            print(e, f", method: {self.get_height.__name__} link: {url}")
            return ""



    def get_width(self, url, soup) -> str:
        """ Get product width. """
        try:
            width = soup.find_all('td', {'width': '302'})[3].string
            return extract_digits(width)
        except IndexError as e:
            try:
                temp = soup.find('div', {'itemprop': 'description'}).contents[4].text.split(": ")[1][4:7]
                width = str(temp)+"0"
                return extract_digits(width)
            except (AttributeError, IndexError):
                return ""
        except (AttributeError, ValueError) as e:
            print(e, f", method: {self.get_height.__name__} link: {url}")
            return ""


    def get_depth(self, url, soup) -> str:
        """ Get product depth. """
        try:
            depth = soup.find_all('td', {'width': '302'})[5].string
            return extract_digits(depth)
        except IndexError as e:
            try:
                depth = soup.find('div', {'itemprop': 'description'}).contents[4].text.split(": ")[1][7:12]
                return extract_digits(depth)
            except (AttributeError, IndexError):
                return ""
        except (AttributeError, ValueError) as e:
            print(e, f", method: {self.get_height.__name__} link: {url}")
            return ""


    def get_description(self, url, soup) -> str:
        """ Get product description. """
        try:
            return soup.find('div', {"itemprop": 'description', "class": "resetcss"}).text
        except (AttributeError, ValueError, IndexError) as e:
            try:
                print(e, f", method: {self.get_height.__name__} link: {url}")
                return soup.find('div', {"class": 'resetcss', "itemprop": "description"}).findChildren("p")[2]
            except (AttributeError, ValueError) as e:
                print(e, f", method: {self.get_height.__name__} link: {url}")
                return ""


    def get_status(self, url, soup):
        """ Get shipping status. """
        try:
            czas_realizacji = ''
            t_ship = str(soup.find('span', {'class': 'second'}).string)
            if t_ship == '48 - 72 H':
                index = t_ship.find("- ")
                czas_realizacji = str(int(t_ship[index + 2:-2]) / 24).split('.')[0]
            if t_ship == '3-4 tygodnie':
                czas_realizacji = t_ship.split('-')[1]
            return czas_realizacji
        except (AttributeError, ValueError) as e:
            print(e, f", method: {self.get_height.__name__} link: {url}")
            return ""

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
        result["DYSTRYBUTOR"] = "Locobox"

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
        result["WYSOKO????"] = self.get_height(url, soup)
        result["SZEROKO????"] = self.get_width(url, soup)
        result["G????BOKO????"] = self.get_depth(url, soup)

        # Characteristics
        result["CECHY CHARAKTERYSTYCZNE"] = self.get_description(url, soup)

        # Source url / price list / catalogue
        result["??R??D??O"] = url

        # Find shipping time

        result["CZAS REALIZACJI [dni]"] = self.get_status(url, soup)

        # Warranty
        result["GWARANCJA [miesi??ce]"] = "60 miesi??cy"

        # Comment
        if result["CENA SKLEPU INTERNETOWEGO NETTO"] != "":
            result["msg"] = self.get_comment(link[1], result["CENA SKLEPU INTERNETOWEGO NETTO"])
        else:
            result["msg"] = ""

        return records.append(result)

    def scrap(self):
        """Scrap through all links in a list."""

        print("Starting scrapping Locobox.")
        i = 0
        for link in links:
            try:
                i += 1
                show_status(i, links)
                self.scrap_link(link)
            except Error as e:
                print(e, f"Something wrong with {link[0]}")


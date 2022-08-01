from bs4 import BeautifulSoup as bs4
import requests
from mc_webscrapper.bakpol.bakpol_links import LINKS
from mc_webscrapper.scrapper_dataclass import ScrapperDataClass
from mc_webscrapper.scrapper_class import ScrapperClass
from mc_webscrapper.config import REQUEST_TIMEOUT, HEADERS
from mc_webscrapper.helpers import show_status, clear_price, extract_digits, save_dataclass_to_file


class Bakpol(ScrapperClass):
    """
    This class represents scrapper of Bakpol (https://bakpol.pl/). It is using BeatifulSoup scrapper to get products data from product's card at online shop.
    """


    stored_data_list: list = []

    def setup_scrapper(self, link: str):
        response = requests.get(link, timeout=REQUEST_TIMEOUT, headers=HEADERS)
        soup = bs4(response.text, 'html.parser')
        return soup

    def get_dealer_name(self) -> str:
        return "Bakpol"

    def get_manufacturer_name(self) -> str:
        return "Bakpol"

    def get_model_name(self, soup) -> str:
        try:
            model = soup.find('h1', {'class': 'nazwa-produktu'}).string.strip()
            return str(model.lower())
        except Exception(f"Something went wrong with getting model name in {soup.title.string}") as e:
            print(e)

    def get_shop_price_nett(self, soup) -> int:
        try:
            nett_price = soup.find('span', {"id": "our_price_display"}).string
            return clear_price(nett_price)
        except Exception(f"Something went wrong with getting price in {soup.title.string}") as e:
            print(e)

    def get_product_height(self, soup):
        try:
            height = soup.find('table', class_='table-data-sheet').find_all('td')[1].text
            return extract_digits(height)
        except (ValueError, AttributeError) as e:
            try:
                height = soup.find('div', {'class': 'rte'}).find('ul').find_all('li')[3]
                height = height.text.split('mm')
                return extract_digits(height[0])
            except (ValueError, AttributeError):
                print(f", method: {self.get_height.__name__} link: {soup.title.string}")
                return ""

    def get_product_width(self, soup):
        try:
            width = soup.find('table', class_='table-data-sheet').find_all('td')[3].text
            return extract_digits(width)
        except (ValueError, AttributeError) as e:
            try:
                width = soup.find('div', {'class': 'rte'}).find('ul').find_all('li')[3]
                width = width.text.split('mm')
                return extract_digits(width[1])
            except (ValueError, AttributeError):
                print(f", method: {self.get_height.__name__} link: {soup.title.string}")
                return ""

    def get_product_depth(self, soup):
        try:
            depth = soup.find('table', class_='table-data-sheet').find_all('td')[5].text
            return extract_digits(depth)
        except (ValueError, AttributeError) as e:
            try:
                depth = soup.find('div', {'class': 'rte'}).find('ul').find_all('li')[3]
                depth = depth.text.split('mm')
                return extract_digits(depth[2])
            except (ValueError, AttributeError):
                print(f", method: {self.get_height.__name__} link: {soup.title.string}")
                return "" 

    def get_product_features(self, soup):
        try:
            desc = soup.find(class_="rte").text
            return str(desc)
        except (ValueError, IndexError) as e:
            print(e, f", method: {self.get_description.__name__} link: {soup.title.string}")
            return ""
 
    def get_lead_time(self):
       return "" 

    def get_product_warranty(self):
        return 24 

    def get_comment(self):
        return ""

    def gather_data_from_link(self, link):
        url = link[0]
        bakpol = ScrapperDataClass(name="Bakpol")
        soup = self.setup_scrapper(url)
        bakpol.dealer = self.get_dealer_name()
        bakpol.manufacturer = self.get_manufacturer_name()
        bakpol.model = self.get_model_name(soup)
        bakpol.substitute = link[1]
        bakpol.catalogue_price_nett = None
        bakpol.shop_price_nett = self.get_shop_price_nett(soup)
        bakpol.product_height = self.get_product_height(soup)
        bakpol.product_width = self.get_product_width(soup)
        bakpol.product_depth = self.get_product_depth(soup)
        bakpol.product_features = self.get_product_features(soup)
        bakpol.product_card_link = url
        bakpol.lead_time = self.get_lead_time()
        bakpol.product_warranty = self.get_product_warranty()
        bakpol.comment = self.get_comment()
        return bakpol

    def save(self):
        save_dataclass_to_file("bakpol", self.stored_data_list)
        return True

    def run(self):
        for counter, link in enumerate(LINKS):
            show_status(counter, LINKS)
            data = self.gather_data_from_link(link)
            self.stored_data_list.append(data)
            self.save()
        return self.stored_data_list

from bs4 import BeautifulSoup as bs4
import requests
from mc_webscrapper.kartmap.kartmap_links import LINKS
from mc_webscrapper.scrapper_dataclass import ScrapperDataClass
from mc_webscrapper.scrapper_class import ScrapperClass
from mc_webscrapper.config import REQUEST_TIMEOUT, HEADERS
from mc_webscrapper.helpers import show_status, clear_price, extract_digits, save_dataclass_to_file


class KartMap(ScrapperClass):
    """
    This class represents scrapper of Kart-Map (https://www.kart-map.pl/). It is using BeatifulSoup scrapper to get products data from product's card at online shop.
    """

    stored_data_list: list = list()
    company_name = "Kart-Map"

    def setup_scrapper(self, link: str):
        response = requests.get(link, timeout=REQUEST_TIMEOUT, headers=HEADERS)
        soup = bs4(response.text, 'html.parser')
        return soup

    def get_dealer_name(self) -> str:
        return self.company_name

    def get_manufacturer_name(self) -> str:
        return self.company_name

    def get_model_name(self, soup) -> str:
        try:
            return soup.find('h1', {'class': 'product_title entry-title'}).text
        except (ValueError, AttributeError):
            print(f", method: {self.get_model_name.__name__} link: {soup.title.string}")

    def get_shop_price_nett(self, soup) -> int:
        try:
            # price = soup.find("span", class_="price").text
            price = soup.find("bdi").text
            if type(price):
                nett_price = clear_price(price)
                return nett_price
        except (ValueError, AttributeError):
            print(f", method: {self.get_shop_price_nett.__name__} link: {soup.title.string}")

    def get_product_height(self, soup):
        try:
            height = soup.find_all('td', {'width': '302'})[1].text
            return extract_digits(height)
        except (ValueError, AttributeError):
            print(f", method: {self.get_shop_price_nett.__name__} link: {soup.title.string}")
        except IndexError:
            return ""

    def get_product_width(self, soup):
        try:
            szerokosc = soup.find_all('td', {'width': '302'})[3].string
            return extract_digits(szerokosc)
        except (ValueError, AttributeError):
            print(f", method: {self.get_shop_price_nett.__name__} link: {soup.title.string}")

    def get_product_depth(self, soup):
        try:
            depth = soup.find_all('td', {'width': '302'})[5].text
            return extract_digits(depth)
        except (ValueError, AttributeError):
            print(f", method: {self.get_shop_price_nett.__name__} link: {soup.title.string}")

    def get_product_features(self, soup):
        try:
            return soup.find(id="tab-description").text
        except (ValueError, AttributeError):
            print(f", method: {self.get_shop_price_nett.__name__} link: {soup.title.string}")
 
    def get_lead_time(self):
        return "Przeciętny czas dostawy 1-4 tygodnie"

    def get_product_warranty(self):
        return 2

    def get_comment(self):
        pass

    def gather_data_from_link(self, link):
        url = link[0]
        kartmap = ScrapperDataClass(name="Kart-Map")
        soup = self.setup_scrapper(url)
        kartmap.dealer = self.get_dealer_name()
        kartmap.manufacturer = self.get_manufacturer_name()
        kartmap.model = self.get_model_name(soup)
        kartmap.substitute = link[1]
        kartmap.catalogue_price_nett = None
        kartmap.shop_price_nett = self.get_shop_price_nett(soup)
        kartmap.product_height = self.get_product_height(soup)
        kartmap.product_width = self.get_product_width(soup)
        kartmap.product_depth = self.get_product_depth(soup)
        kartmap.product_features = self.get_product_features(soup)
        kartmap.product_card_link = url
        kartmap.lead_time = self.get_lead_time()
        kartmap.product_warranty = self.get_product_warranty()
        kartmap.comment = self.get_comment()
        return kartmap

    def save(self):
        save_dataclass_to_file("kart_map", self.stored_data_list)
        return True

    def run(self):
        for counter, link in enumerate(LINKS):
            show_status(counter, LINKS)
            data = self.gather_data_from_link(link)
            self.stored_data_list.append(data)
            self.save()
        return self.stored_data_list
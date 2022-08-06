from bs4 import BeautifulSoup as bs4
import requests
from mc_webscrapper.kartmap.kartmap_links import LINKS
from mc_webscrapper.scrapper_dataclass import ScrapperDataClass
from mc_webscrapper.scrapper_class import ScrapperClass
from mc_webscrapper.config import REQUEST_TIMEOUT, HEADERS
from mc_webscrapper.helpers import show_status, clear_price, extract_digits, save_dataclass_to_file


class Umstahl():
    """
    This class represents scrapper of Umstahl (https://umstahl.pl/). It is using BeatifulSoup scrapper to get products data from product's card at online shop.
    """

    stored_data_list: list = list()
    company_name = "Umstahl"

    def setup_scrapper(self, link: str):
        response = requests.get(link, timeout=REQUEST_TIMEOUT, headers=HEADERS)
        soup = bs4(response.text, 'html.parser')
        return soup

    def get_dealer_name(self) -> str:
        return self.company_name

    def get_manufacturer_name(self) -> str:
        return self.company_name

    def get_model_name(self, soup) -> str:
        pass

    def get_shop_price_nett(self, soup) -> int:
        pass

    def get_product_height(self, soup):
        pass

    def get_product_width(self, soup):
        pass

    def get_product_depth(self, soup):
        pass

    def get_product_features(self, soup):
        pass
 
    def get_lead_time(self):
        pass

    def get_product_warranty(self):
        return 3

    def get_comment(self):
        pass

    def gather_data_from_link(self, link):
        url = link[0]
        umstahl = ScrapperDataClass(name="Umstahl")
        soup = self.setup_scrapper(url)
        umstahl.dealer = self.get_dealer_name()
        umstahl.manufacturer = self.get_manufacturer_name()
        umstahl.model = self.get_model_name(soup)
        umstahl.substitute = link[1]
        umstahl.catalogue_price_nett = None
        umstahl.shop_price_nett = self.get_shop_price_nett(soup)
        umstahl.product_height = self.get_product_height(soup)
        umstahl.product_width = self.get_product_width(soup)
        umstahl.product_depth = self.get_product_depth(soup)
        umstahl.product_features = self.get_product_features(soup)
        umstahl.product_card_link = url
        umstahl.lead_time = self.get_lead_time()
        umstahl.product_warranty = self.get_product_warranty()
        umstahl.comment = self.get_comment()
        return umstahl

    def save(self):
        save_dataclass_to_file("umstahl", self.stored_data_list)
        return True

    def run(self):
        for counter, link in enumerate(LINKS):
            show_status(counter, LINKS)
            data = self.gather_data_from_link(link)
            self.stored_data_list.append(data)
            self.save()
        return self.stored_data_list
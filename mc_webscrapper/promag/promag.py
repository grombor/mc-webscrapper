from bs4 import BeautifulSoup as bs4
import requests
from mc_webscrapper.promag.promag_links import LINKS
from mc_webscrapper.scrapper_dataclass import ScrapperDataClass
from mc_webscrapper.scrapper_class import ScrapperClass
from mc_webscrapper.config import REQUEST_TIMEOUT, HEADERS
from mc_webscrapper.helpers import show_status, clear_price, extract_digits, save_dataclass_to_file


class Promag(ScrapperClass):
    """
    This class represents scrapper of Promag (https://e-promag.pl/). It is using BeatifulSoup scrapper to get products data from product's card at online shop.
    """


    stored_data_list: list = list()

    def setup_scrapper(self, link: str):
        response = requests.get(link, timeout=REQUEST_TIMEOUT, headers=HEADERS)
        soup = bs4(response.text, 'html.parser')
        return soup

    def get_dealer_name(self) -> str:
        return "Promag"

    def get_manufacturer_name(self) -> str:
        return "Promag"

    def get_model_name(self, soup) -> str:
        try:
            model = soup.find("h1", attrs={"itemprop": "name"}).parent.find("div", class_="subtitle").string.strip()
            return str(model).lower()
        except:
            model = soup.find_all("h1", attrs={"itemprop": "name"}).string
            return model.lower()


    def get_shop_price_nett(self, soup) -> int:
        try:
            nett_price = soup.find('span', {"itemprop": "price"}).string
            return extract_digits(nett_price)
        except Exception:
            print(f"Error in method: {self.get_shop_price_nett.__name__} link: {soup.title.string}")
            return ""

    def get_product_height(self, soup):
        try:
            height = soup.find_all("div", class_="col-xs-5 value")[3].string.split("mm")[0].strip()
            return extract_digits(height)
        except Exception:
            print(f"Error in method: {self.get_product_height.__name__} link: {soup.title.string}")
            return ""

    def get_product_width(self, soup):
        try:
            width = soup.find_all("div", class_="col-xs-5 value")[0].string.split("mm")[0].strip()
            return extract_digits(width)
        except Exception:
            print(f"Error in method: {self.get_product_width.__name__} link: {soup.title.string}")
            return ""

    def get_product_depth(self, soup):
        try:
            depth = soup.find_all("div", class_="col-xs-5 value")[4].string.split("mm")[0].strip()
            return extract_digits(depth)
        except Exception:
            print(f"Error in method: {self.get_product_depth.__name__} link: {soup.title.string}")
            return ""

    def get_product_features(self, soup):
        try:
            desc = soup.find("div", {"itemprop": "description"}).text
            return str(desc)
        except:
            print(f"Error in method: {self.get_product_features.__name__} link: {soup.title.string}")
            return ""
 
    def get_lead_time(self):
       return ""

    def get_product_warranty(self):
        return 2 

    def get_comment(self):
        return ""

    def gather_data_from_link(self, link):
        url = link[0]
        promag = ScrapperDataClass(name="Promag")
        soup = self.setup_scrapper(url)
        promag.dealer = self.get_dealer_name()
        promag.manufacturer = self.get_manufacturer_name()
        promag.model = self.get_model_name(soup)
        promag.substitute = link[1]
        promag.catalogue_price_nett = None
        promag.shop_price_nett = self.get_shop_price_nett(soup)
        promag.product_height = self.get_product_height(soup)
        promag.product_width = self.get_product_width(soup)
        promag.product_depth = self.get_product_depth(soup)
        promag.product_features = self.get_product_features(soup)
        promag.product_card_link = url
        promag.lead_time = self.get_lead_time()
        promag.product_warranty = self.get_product_warranty()
        promag.comment = self.get_comment()
        return promag

    def save(self):
        save_dataclass_to_file("promag", self.stored_data_list)
        print(f'\n ---------------------------------------- \n')
        return True

    def run(self):
        for counter, link in enumerate(LINKS):
            show_status(counter, LINKS)
            data = self.gather_data_from_link(link)
            self.stored_data_list.append(data)
            self.save()
        return self.stored_data_list

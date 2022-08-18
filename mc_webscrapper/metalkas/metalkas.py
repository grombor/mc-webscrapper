from bs4 import BeautifulSoup as bs4
import requests
from mc_webscrapper.metalkas.metalkas_links import LINKS
from mc_webscrapper.scrapper_dataclass import ScrapperDataClass
from mc_webscrapper.scrapper_class import ScrapperClass
from mc_webscrapper.config import REQUEST_TIMEOUT, HEADERS
from mc_webscrapper.helpers import show_status, clear_price, extract_digits, save_dataclass_to_file


class Metalkas(ScrapperClass):
    """
    This class represents scrapper of Metalkas (https://www.metalkas.com.pl/). It is using BeatifulSoup scrapper to get products data from product's card at online shop.
    """

    stored_data_list: list = list()
    company_name = "Metalkas"


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
            return soup.find('span', {'class': 'base'}).string
        except (ValueError, AttributeError):
            print(f", method: {self.get_model_name.__name__} link: {soup.title.string}")

    def get_shop_price_nett(self, soup) -> int: 
        try:
            price_gross = soup.find('span', class_="price").text
            price_gross = price_gross.split(',')[0]
            price_nett = int(int(price_gross) / 1.3)
            return price_nett
        except (IndexError, TypeError) :
            netto = soup.find("div", {"class": "price-netto"}).text
            price = str(netto).split(',')
            return extract_digits(price[0])
        except (ValueError, AttributeError):
            print(f", method: {self.get_shop_price_nett.__name__} link: {soup.title.string}")

    def get_product_height(self, soup):
        try:
            height = soup.find('td', {'data-th': 'Wysokość zewnętrzna [mm]'}).text
            return extract_digits(height)
        except Exception:
            print(f", method: {self.get_product_height.__name__} link: {soup.title.string}")

    def get_product_width(self, soup):
        try:
            width = soup.find('td', {'data-th': 'Szerokość zewnętrzna [mm]'}).text
            return extract_digits(width)
        except Exception:
            print(f", method: {self.get_product_width.__name__} link: {soup.title.string}")

    def get_product_depth(self, soup):
        try:
            depth = soup.find('td', {'data-th': 'Głębokość zewnętrzna'}).text
            return extract_digits(depth)
        except Exception:
            print(f", method: {self.get_product_depth.__name__} link: {soup.title.string}")

    def get_product_features(self, soup):
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
        except Exception:
            print(f", method: {self.get_shop_price_nett.__name__} link: {soup.title.string}")
 
    def get_lead_time(self, soup):
        try:
            return soup.find('td', {'data-th': 'Czas realizacji'}).text
        except Exception:
            print(f", method: {self.get_lead_time.__name__} link: {soup.title.string}")

    def get_product_warranty(self):
        return 2

    def get_comment(self):
        pass

    def gather_data_from_link(self, link):
        url = link[0]
        metalkas = ScrapperDataClass(name="Metalkas")
        soup = self.setup_scrapper(url)
        metalkas.dealer = self.get_dealer_name()
        metalkas.manufacturer = self.get_manufacturer_name()
        metalkas.model = self.get_model_name(soup)
        metalkas.substitute = link[1]
        metalkas.catalogue_price_nett = None
        metalkas.shop_price_nett = self.get_shop_price_nett(soup)
        metalkas.product_height = self.get_product_height(soup)
        metalkas.product_width = self.get_product_width(soup)
        metalkas.product_depth = self.get_product_depth(soup)
        metalkas.product_features = self.get_product_features(soup)
        metalkas.product_card_link = url
        metalkas.lead_time = self.get_lead_time()
        metalkas.product_warranty = self.get_product_warranty()
        metalkas.comment = self.get_comment()
        return metalkas

    def save(self):
        save_dataclass_to_file("metalkas", self.stored_data_list)
        return True

    def run(self):
        for counter, link in enumerate(LINKS):
            show_status(counter, LINKS)
            data = self.gather_data_from_link(link)
            self.stored_data_list.append(data)
            self.save()
        return self.stored_data_list
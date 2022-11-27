from bs4 import BeautifulSoup as bs4
import requests
from mc_webscrapper.jotkel.jotkel_links import LINKS
from mc_webscrapper.scrapper_dataclass import ScrapperDataClass
from mc_webscrapper.scrapper_class import ScrapperClass
from mc_webscrapper.config import REQUEST_TIMEOUT, HEADERS
from mc_webscrapper.helpers import show_status, clear_price, extract_digits, save_dataclass_to_file
import string


class Jotkel(ScrapperClass):
    """
    This class represents scrapper of JotKEL (https://jotkel.com/). It is using BeatifulSoup scrapper to get products data from product's card at online shop.
    """

    stored_data_list: list = list()
    company_name = "Jotkel"

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
            model = soup.find('h1', {'class': 'name'}).text
            temp = str(model).strip().replace("\\n", "")
            return temp.lower()
        except Exception as e:
            print(e)

    def get_shop_price_nett(self, soup) -> int:
        try:
            brutto = soup.find("em", {"class": "main-price"}).text.split(',')[0]
            brutto = extract_digits(brutto)
            return int(int(brutto) / 1.23)
        except AttributeError as e:
            try:
                pass
            except Exception as e:
                print(e)

    def get_product_height(self, soup):
        try:
            height = soup.find_all("td", {"class": "DataGridWlascColWartoscItemStyle"})[1]
            height = extract_digits(height)
            return height
        except (ValueError, AttributeError):
            print(f", method: {self.get_height.__name__} link: {soup.title.string}")
            return ""

    def get_product_width(self, soup):
        try:
            width = soup.find_all("td", {"class": "DataGridWlascColWartoscItemStyle"})[0]
            width = extract_digits(width)
            return width
        except (ValueError, AttributeError):
            print(f", method: {self.get_height.__name__} link: {soup.title.string}")
            return ""

    def get_product_depth(self, soup):
        """ Get product depth. """
        try:
            depth = soup.find_all("td", {"class": "DataGridWlascColWartoscItemStyle"})[2]
            depth = extract_digits(depth)
            return depth
        except (ValueError, AttributeError):
            print(f", method: {self.get_height.__name__} link: {soup.title.string}")
            return ""

    def get_product_features(self, soup):
        try:
            features = soup.find_all({"class": "resetcss"})
            return features
        except (ValueError, IndexError) as e:
            print(e, f", method: {self.get_product_features.__name__} link: {soup.title.string}")
            return ""

    def get_lead_time(self, soup):
        try:
            lead_time = soup.find("div", class_="delivery").find("span", "second").text
            return lead_time
        except (ValueError, IndexError, AttributeError):
            try:
                lead_time = soup.find("p", class_="status").text
                return lead_time
            except (ValueError, IndexError, AttributeError):
                print(f", method: get_lead_time")
            return ""

    def get_product_warranty(self):
        return 24

    def get_comment(self):
        return "Firma posiada w swojej ofercie meble wymagające samodzielnego montażu."

    def gather_data_from_link(self, link):
        url = link[0]
        jotkel = ScrapperDataClass(name="Jotkel")
        soup = self.setup_scrapper(url)
        jotkel.dealer = self.get_dealer_name()
        jotkel.manufacturer = self.get_manufacturer_name()
        jotkel.model = self.get_model_name(soup)
        jotkel.substitute = link[1]
        jotkel.catalogue_price_nett = None
        jotkel.shop_price_nett = self.get_shop_price_nett(soup)
        jotkel.product_height = self.get_product_height(soup)
        jotkel.product_width = self.get_product_width(soup)
        jotkel.product_depth = self.get_product_depth(soup)
        jotkel.product_features = self.get_product_features(soup)
        jotkel.product_card_link = url
        jotkel.lead_time = self.get_lead_time(soup)
        jotkel.product_warranty = self.get_product_warranty()
        jotkel.comment = self.get_comment()
        return jotkel

    def save(self):
        save_dataclass_to_file("jotkel", self.stored_data_list)
        print(f'\n ---------------------------------------- \n')
        return True

    def run(self):
        for counter, link in enumerate(LINKS):
            show_status(counter, LINKS)
            data = self.gather_data_from_link(link)
            self.stored_data_list.append(data)
            self.save()
        return self.stored_data_list
from bs4 import BeautifulSoup as bs4
import requests
from mc_webscrapper.jan_nowak.jannowak_links import LINKS
from mc_webscrapper.scrapper_dataclass import ScrapperDataClass
from mc_webscrapper.scrapper_class import ScrapperClass
from mc_webscrapper.config import REQUEST_TIMEOUT, HEADERS
from mc_webscrapper.helpers import show_status, clear_price, extract_digits, save_dataclass_to_file


class JanNowak(ScrapperClass):
    """
    This class represents scrapper of Jan Nowak (https://jannowak.com/). It is using BeatifulSoup scrapper to get products data from product's card at online shop.
    """

    stored_data_list: list = list()
    company_name = "Jan Nowak"

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
            model = soup.find('form', {'id': 'product-cart-form'}).find('p').contents
            temp_string = str(model).replace("\\n", "")
            temp_index = str(temp_string).find('Model')
            model = temp_string[temp_index + 6:-2]
            return model.lower()
        except Exception as e:
            print(e)

    def get_shop_price_nett(self, soup) -> int:
        try:
            brutto = soup.find('div', {"class": "pricing"}).find('p', {"class": "current-price js-price"}).string.replace(" ", "").split(",")[0]
            brutto = extract_digits(brutto)
            return int(int(brutto)/1.23)
        except AttributeError as e:
            try:
                brutto = soup.find('div', {"class": "pricing"}).find('p', {"class": "current-price js-price"}).text.split(",")[0]
                brutto = extract_digits(brutto)
                return int(int(brutto) / 1.23)
            except Exception as e:
                print(e)

    def get_product_height(self, soup):
        try:
            height = soup.find_all("p", {"class": "normal"})[0].text
            height = extract_digits(height)
            return height*10
        except (ValueError, AttributeError):
            print(f", method: {self.get_height.__name__} link: {soup.title.string}")
            return ""

    def get_product_width(self, soup):
        try:
            width = soup.find_all("p", class_="normal")[1].text[:-2]
            width = extract_digits(width)
            return width*10
        except (ValueError, AttributeError):
            print(f", method: {self.get_height.__name__} link: {soup.title.string}")
            return ""

    def get_product_depth(self, soup):
        """ Get product depth. """
        try:
            depth = soup.find_all("p", class_="normal")[2].text[:-2]
            depth = extract_digits(depth)
            return depth*10
        except (ValueError, AttributeError):
            print(f", method: {self.get_height.__name__} link: {soup.title.string}")
            return "" 

    def get_product_features(self, soup):
        try:
            return soup.find(class_="product-desc").text[1:]
        except (ValueError, IndexError) as e:
            print(e, f", method: {self.get_description.__name__} link: {soup.title.string}")
            return ""
 
    def get_lead_time(self, soup):
        try:
            lead_time = soup.find("p", class_="status").text.split(" w ")
            return lead_time[1]
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
        jannowak = ScrapperDataClass(name="Jan Nowak")
        soup = self.setup_scrapper(url)
        jannowak.dealer = self.get_dealer_name()
        jannowak.manufacturer = self.get_manufacturer_name()
        jannowak.model = self.get_model_name(soup)
        jannowak.substitute = link[1]
        jannowak.catalogue_price_nett = None
        jannowak.shop_price_nett = self.get_shop_price_nett(soup)
        jannowak.product_height = self.get_product_height(soup)
        jannowak.product_width = self.get_product_width(soup)
        jannowak.product_depth = self.get_product_depth(soup)
        jannowak.product_features = self.get_product_features(soup)
        jannowak.product_card_link = url
        jannowak.lead_time = self.get_lead_time(soup)
        jannowak.product_warranty = self.get_product_warranty()
        jannowak.comment = self.get_comment()
        return jannowak

    def save(self):
        save_dataclass_to_file("jan_nowak", self.stored_data_list)
        print(f'\n ---------------------------------------- \n')
        return True

    def run(self):
        for counter, link in enumerate(LINKS):
            show_status(counter, LINKS)
            data = self.gather_data_from_link(link)
            self.stored_data_list.append(data)
            self.save()
        return self.stored_data_list
        
from bs4 import BeautifulSoup as bs4
import requests
from mc_webscrapper.locobox.locobox_links import LINKS
from mc_webscrapper.scrapper_dataclass import ScrapperDataClass
from mc_webscrapper.scrapper_class import ScrapperClass
from mc_webscrapper.config import REQUEST_TIMEOUT, HEADERS
from mc_webscrapper.helpers import show_status, extract_digits, save_dataclass_to_file


class LocoBox(ScrapperClass):
    """
    This class represents scrapper of Locobox (https://locobox.pl/). It is using BeatifulSoup scrapper to get products data from product's card at online shop.
    """

    stored_data_list: list = list()
    company_name = "Locobox"


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
            return soup.find('h1', {'class': 'name'}).string.strip().lower()
        except (ValueError, AttributeError):
            print(f"method: {self.get_model_name.__name__} link: {soup.title.string}")

    def get_shop_price_nett(self, soup) -> int: 
        try:
            netto = soup.find("div", class_="price-netto")
            price = netto.text.split(",")[0]
            return extract_digits(price)
        except IndexError:
            netto = soup.find("div", {"class": "price-netto"}).text
            price = str(netto).split(',')
            return extract_digits(price[0])
        except (ValueError, AttributeError):
            print(f"method: {self.get_shop_price_nett.__name__} link: {soup.title.string}")

    def get_product_height(self, soup):
        try:
            height = soup.find_all('td', {'width': '302'})[1].text
            return extract_digits(height)
        except IndexError as e:
            try:
                temp = soup.find('div', {'itemprop': 'description'}).contents[4].text.split(": ")[1]
                height = str(temp)[:3]+"0"
                return extract_digits(height)
            except (AttributeError, IndexError):
                try:
                    temp = soup.find('div', {'itemprop': 'description'}).contents[6].text.split(": ")[1]
                    height = str(temp)[:3]+"0"
                    return extract_digits(height)
                except (AttributeError, ValueError, IndexError):
                    return ""
        except Exception:
            print(f"method: {self.get_product_height.__name__} link: {soup.title.string}")

    def get_product_width(self, soup):
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
        except Exception:
            print(f"method: {self.get_product_width.__name__} link: {soup.title.string}")

    def get_product_depth(self, soup):
        try:
            depth = soup.find_all('td', {'width': '302'})[5].string
            return extract_digits(depth)
        except IndexError as e:
            try:
                depth = soup.find('div', {'itemprop': 'description'}).contents[4].text.split(": ")[1][7:12]
                return extract_digits(depth)
            except (AttributeError, IndexError):
                return ""
        except Exception:
            print(f"method: {self.get_product_depth.__name__} link: {soup.title.string}")

    def get_product_features(self, soup):
        try:
            return soup.find('div', {"itemprop": 'description', "class": "resetcss"}).text
        except (AttributeError, ValueError, IndexError) as e:
            try:
                print(e, f"method: {self.get_height.__name__} link: {url}")
                return soup.find('div', {"class": 'resetcss', "itemprop": "description"}).findChildren("p")[2]
            except (AttributeError, ValueError) as e:
                print(e, f"method: {self.get_height.__name__} link: {url}")
                return ""
        except Exception:
            print(f"method: {self.get_shop_price_nett.__name__} link: {soup.title.string}")
 
    def get_lead_time(self, soup):
        lead_time = soup.find("div", {"class": "delivery"}).find("span", class_="second").text
        return lead_time

    def get_product_warranty(self):
        return 2

    def get_comment(self):
        pass

    def gather_data_from_link(self, link):
        url = link[0]
        locobox = ScrapperDataClass(name=self.company_name)
        soup = self.setup_scrapper(url)
        locobox.dealer = self.get_dealer_name()
        locobox.manufacturer = self.get_manufacturer_name()
        locobox.model = self.get_model_name(soup)
        locobox.substitute = link[1]
        locobox.catalogue_price_nett = None
        locobox.shop_price_nett = self.get_shop_price_nett(soup)
        locobox.product_height = self.get_product_height(soup)
        locobox.product_width = self.get_product_width(soup)
        locobox.product_depth = self.get_product_depth(soup)
        locobox.product_features = self.get_product_features(soup)
        locobox.product_card_link = url
        locobox.lead_time = self.get_lead_time(soup)
        locobox.product_warranty = self.get_product_warranty()
        locobox.comment = self.get_comment()
        return locobox

    def save(self):
        save_dataclass_to_file("locobox", self.stored_data_list)
        return True

    def run(self):
        for counter, link in enumerate(LINKS):
            show_status(counter, LINKS)
            data = self.gather_data_from_link(link)
            self.stored_data_list.append(data)
            self.save()
        return self.stored_data_list
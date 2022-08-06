# from bs4 import BeautifulSoup as bs4
# import requests
# from mc_webscrapper.jannowak_links import links
# from mc_webscrapper.utils import get_date, compare_prices, records, show_status, requests_timeout, extract_digits
# from mc_webscrapper.errors import Error


# class JanNowak:
#     """ This class represents products of Jan Nowak manufacturer & dealer (https://jannowak.com/)"""


#     def get_links(self) -> list:
#         """ Import links from a file."""
#         try:
#             if len(links) <= 0:
#                 raise Error("Links list is empty or broken.")
#             return links
#         except Error as e:
#             print(e)


#     def get_model(self, url, soup) -> str:
#         """ Get product model. """
#         try:
#             model = soup.find('form', {'id': 'product-cart-form'}).find('p').contents
#             temp_string = str(model).replace("\\n", "")
#             temp_index = str(temp_string).find('Model')
#             model = temp_string[temp_index + 6:-2]
#             return model
#             raise Error(f"Something wrong with product name in {url}.")
#         except ValueError as e:
#             print(e, f", method: {self.get_model.__name__} link: {url}")
#             return ""


#     def get_price(self, url, soup):
#         """ Get product price. """
#         try:
#             brutto = soup.find('div', {"class": "pricing"}).find('p', {"class": "current-price js-price"}).string.replace(" ", "").split(",")[0]
#             brutto = extract_digits(brutto)
#             return int(int(brutto)/1.23)
#         except AttributeError as e:
#             try:
#                 brutto = soup.find('div', {"class": "pricing"}).find('p', {"class": "current-price js-price"}).text.split(",")[0]
#                 brutto = extract_digits(brutto)
#                 return int(int(brutto) / 1.23)
#             except AttributeError as e:
#                 print(e, f", method: {self.get_price.__name__} link: {url}")
#                 return ""


#     def get_height(self, url, soup) -> str:
#         """ Get product height. """
#         try:
#             height = soup.find_all("p", class_="normal")[0].text[:-2]
#             height = extract_digits(height)
#             return height+"0"
#         except (AttributeError, TypeError, ValueError) as e:
#             print(e, f", method: {self.get_height.__name__} link: {url}")
#             return ""


#     def get_width(self, url, soup) -> str:
#         """ Get product width. """
#         try:
#             width = soup.find_all("p", class_="normal")[1].text[:-2]
#             width = extract_digits(width)
#             return width+"0"
#         except (ValueError, AttributeError, TypeError) as e:
#             print(e, f", method: {self.get_width.__name__} link: {url}")
#             return ""


#     def get_depth(self, url, soup) -> str:
#         """ Get product depth. """
#         try:
#             depth = soup.find_all("p", class_="normal")[2].text[:-2]
#             depth = extract_digits(depth)
#             return depth+"0"
#         except (ValueError, IndexError, AttributeError, TypeError) as e:
#             print(e, f", method: {self.get_depth.__name__} link: {url}")
#             return ""


#     def get_description(self, url, soup) -> str:
#         """ Get product description. """
#         try:
#             return soup.find(class_="product-desc").text[1:]
#         except (ValueError, IndexError, AttributeError) as e:
#             print(e, f", method: {self.get_description.__name__} link: {url}")
#             return ""


#     def get_status(self, url, soup):
#         """ Get shipping status. """
#         try:
#             return soup.find("p", class_="status").text
#         except (ValueError, IndexError, AttributeError) as e:
#             print(e, f", method: {self.get_description.__name__} link: {url}")
#             return ""


#     def get_comment(self, previous_price, nett, url) -> str:
#         """ Create product comment. """
#         try:
#             if previous_price == nett:
#                 return ""
#             else:
#                 return compare_prices(nett, previous_price)
#         except (ValueError, IndexError) as e:
#             print(e, f", method: {self.get_depth.__name__} link: {url}")
#             return ""


#     def scrap_link(self, link):
#         """ Scraps given url, gathers all data and create dictionary record. """

#         result = dict()

#         # Save current dealer
#         result["DYSTRYBUTOR"] = "Jan Nowak"

#         # Save current date
#         result["DATA"] = get_date()

#         # Use requests to retrieve data from a given URL
#         url = link[0]
#         headers = requests.utils.default_headers()
#         headers.update({
#             'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
#         })
#         response = requests.get(url, timeout=requests_timeout, headers=headers)

#         # Parse the whole HTML page using BeautifulSoup
#         soup = bs4(response.text, 'html.parser')

#         # Parse product name
#         result["MODEL"] = self.get_model(url, soup)

#         # Is comparable with
#         result["ODPOWIEDNIK"] = link[2]

#         # If position is not from price list of catalogue - leave it empty
#         result["CENA KATALOGOWA NETTO"] = ""

#         # Current product price
#         result["CENA SKLEPU INTERNETOWEGO NETTO"] = self.get_price(url, soup)

#         # If position is not from price list of catalogue - leave it empty
#         result["RABAT"] = ""
#         result["CENA KATALOGOWA PO RABACIE"] = ""

#         # Find dimmensions
#         result["WYSOKOŚĆ"] = self.get_height(url, soup)
#         result["SZEROKOŚĆ"] = self.get_width(url, soup)
#         result["GŁĘBOKOŚĆ"] = self.get_depth(url, soup)

#         # Characteristics
#         result["CECHY CHARAKTERYSTYCZNE"] = self.get_description(url, soup)

#         # Source url / price list / catalogue
#         result["ŹRÓDŁO"] = url

#         # Find shipping time
#         result["CZAS REALIZACJI [dni]"] = self.get_status(url, soup)

#         # Warranty
#         result["GWARANCJA [miesiące]"] = "6"

#         # Comment
#         if result["CENA SKLEPU INTERNETOWEGO NETTO"] != "":
#             result["msg"] = self.get_comment(link[1], result["CENA SKLEPU INTERNETOWEGO NETTO"], url)
#         else:
#             result["msg"] = ""

#         return records.append(result)


#     def scrap(self):
#         """Scrap through all links in a list."""

#         print("Starting scrapping Jan Nowak.")
#         i = 0
#         for link in links:
#             try:
#                 i += 1
#                 show_status(i, links)
#                 self.scrap_link(link)
#             except Error as e:
#                 print(e, f"Something wrong with {link[0]}")


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
        return True

    def run(self):
        for counter, link in enumerate(LINKS):
            show_status(counter, LINKS)
            data = self.gather_data_from_link(link)
            self.stored_data_list.append(data)
            self.save()
        return self.stored_data_list
        
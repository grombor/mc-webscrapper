import random
import pytest
from bs4 import BeautifulSoup as bs4
import requests
from mc_webscrapper.scrapper_dataclass import ScrapperDataClass
from mc_webscrapper.promag.promag_links import LINKS
from mc_webscrapper.promag.promag import Promag


LINK = ("https://e-promag.pl/katalog/Szafka-BHP-pracownicza-SUPE300-02-7035,2831.html", "SUM 320W")
HTML = requests.get(LINK[0])
SOUP = bs4(HTML.text, 'html.parser')
promag = Promag()

def test_LINKS():
    link = random.choice(LINKS)
    assert link

def test_setup_scrapper():
    if SOUP:
        assert isinstance(SOUP, bs4)

def test_gather_data_from_link_dataclass():
    b = ScrapperDataClass(name="Promag")
    assert isinstance(b, ScrapperDataClass)

def test_dealer_name():
    assert promag.get_dealer_name() == "Promag"

def test_get_manufacturer_name():
    assert promag.get_manufacturer_name() == "Promag"

def test_get_model_name():
    model = promag.get_model_name(SOUP).lower()
    assert model == "SUPE 300-02".lower()

def test_get_shop_price_nett():
    price_nett = promag.get_shop_price_nett(SOUP)
    assert price_nett == 490

def test_get_product_height():
    height = promag.get_product_height(SOUP)
    assert height == 1800

def test_get_product_width():
    width = promag.get_product_width(SOUP)
    assert width == 600

def test_get_product_depth():
    depth = promag.get_product_depth(SOUP)
    assert depth == 480

def test_get_product_features():
    features = promag.get_product_features(SOUP)
    assert (features != "") and features is not None

def test_get_lead_time():
    lead_time = promag.get_lead_time()
    assert lead_time == ""

def test_get_product_warranty():
    assert promag.get_product_warranty() == 2

def test_get_comment():
    assert promag.get_comment() == ""

def test_save():
    assert promag.save()

def test_run():
    assert isinstance(promag.run(), list)
import random
import pytest
from bs4 import BeautifulSoup as bs4
import requests
from mc_webscrapper.scrapper_dataclass import ScrapperDataClass
from mc_webscrapper.jan_nowak.jannowak_links import LINKS
from mc_webscrapper.umstahl.umstahl import Umstahl


LINK = ("https://www.kart-map.pl/produkt/szafa-ubraniowa-bhp-dwudrzwiowa/", "SUM 320")
HTML = requests.get(LINK[0])
SOUP = bs4(HTML.text, 'html.parser')
us = Umstahl()

def test_LINKS():
    link = random.choice(LINKS)
    assert link

def test_setup_scrapper():
    if SOUP:
        assert isinstance(SOUP, bs4)

def test_gather_data_from_link_dataclass():
    b = ScrapperDataClass(name="Umstahl")
    assert isinstance(b, ScrapperDataClass)

def test_dealer_name():
    assert us.get_dealer_name() == "Umstahl"

def test_get_manufacturer_name():
    assert us.get_manufacturer_name() == "Umstahl"

# def test_get_model_name():
#     model = us.get_model_name(SOUP).lower()
#     assert model == "SZAFA UBRANIOWA BHP DWUDRZWIOWA".lower()

# def test_get_shop_price_nett():
#     price_nett = us.get_shop_price_nett(SOUP)
#     assert price_nett == int(778)

# def test_get_product_height():
#     height = us.get_product_height(SOUP)
#     assert height == 1800

# def test_get_product_width():
#     width = us.get_product_width(SOUP)
#     assert width == 600

# def test_get_product_depth():
#     depth = us.get_product_depth(SOUP)
#     assert depth == 490

# def test_get_product_features():
#     features = us.get_product_features(SOUP)
#     assert (features != "") and features is not None

# def test_get_lead_time():
#     lead_time = us.get_lead_time()
#     assert lead_time == "Przeciętny czas dostawy 1-4 tygodnie"

def test_get_product_warranty():
    assert us.get_product_warranty() == 3

# @pytest.mark.skip()
# def test_get_comment():
#     pass

# def test_save():
#     assert us.save()

# def test_run():
#     assert isinstance(us.run(), list)
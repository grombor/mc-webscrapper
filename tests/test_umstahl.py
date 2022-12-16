import random
import pytest
from bs4 import BeautifulSoup as bs4
import requests
from mc_webscrapper.scrapper_dataclass import ScrapperDataClass
from mc_webscrapper.umstahl.umstahl_links import LINKS
from mc_webscrapper.umstahl.umstahl import Umstahl


LINK = ("https://umstahl.pl/metalowa-szafka-ubraniowa-se-30r2-24h,id102.html", "SUM 320")
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

def test_get_model_name():
    model = us.get_model_name(SOUP).lower()
    assert model == "Metalowa szafka ubraniowa SE 30R2".lower()

def test_get_shop_price_nett():
    price_nett = us.get_shop_price_nett(SOUP)
    assert price_nett == int(566)

def test_get_product_height():
    height = us.get_product_height(SOUP)
    assert height == 1800

def test_get_product_width():
    width = us.get_product_width(SOUP)
    assert width == 800

def test_get_product_depth():
    depth = us.get_product_depth(SOUP)
    assert depth == 490

def test_get_product_features():
    features = us.get_product_features(SOUP)
    print(features)
    assert features == ''

def test_get_lead_time():
    lead_time = us.get_lead_time(SOUP)
    assert lead_time == "5-10 dni roboczych (dla zamówienia do 5 sztuk). W przypadku szaf marki C+P dostawa nie obejmuje rozładunku i wniesienia towaru."

def test_get_product_warranty():
    assert us.get_product_warranty() == 3

@pytest.mark.skip()
def test_get_comment():
    pass

def test_save():
    assert us.save()

def test_run():
    assert isinstance(us.run(), list)
import random
import pytest
from bs4 import BeautifulSoup as bs4
import requests
from mc_webscrapper.scrapper_dataclass import ScrapperDataClass
from mc_webscrapper.umstahl.umstahl_links import LINKS
from mc_webscrapper.jotkel.jotkel import Jotkel


LINK = ("https://sklep.jotkel.com/JOTKL-Szafa-ubraniowa-24083_D", "SUM 320W")
HTML = requests.get(LINK[0])
SOUP = bs4(HTML.text, 'html.parser')
jk = Jotkel()

def test_LINKS():
    link = random.choice(LINKS)
    assert link

def test_setup_scrapper():
    if SOUP:
        assert isinstance(SOUP, bs4)

def test_gather_data_from_link_dataclass():
    b = ScrapperDataClass(name="Jotkel")
    assert isinstance(b, ScrapperDataClass)

def test_dealer_name():
    assert jk.get_dealer_name() == "Jotkel"

def test_get_manufacturer_name():
    assert jk.get_manufacturer_name() == "Jotkel"

def test_get_model_name():
    model = jk.get_model_name(SOUP).lower()
    print(model)
    assert model == "SZAFA UBRANIOWA 24083 JOTKEL _D".lower()

def test_get_shop_price_nett():
    price_nett = jk.get_shop_price_nett(SOUP)
    assert price_nett == 807

def test_get_product_height():
    height = jk.get_product_height(SOUP)
    assert height == 1800

def test_get_product_width():
    width = jk.get_product_width(SOUP)
    assert width == 600

def test_get_product_depth():
    depth = jk.get_product_depth(SOUP)
    assert depth == 480

def test_get_product_features():
    features = jk.get_product_features(SOUP)
    print(len(features))
    assert (features == "") and features

def test_get_lead_time():
    lead_time = jk.get_lead_time(SOUP)
    assert lead_time == "2 dni robocze"

def test_get_product_warranty():
    assert jk.get_product_warranty() == 2

@pytest.mark.skip()
def test_get_comment():
    pass

def test_save():
    assert jk.save()

def test_run():
    assert isinstance(jk.run(), list)

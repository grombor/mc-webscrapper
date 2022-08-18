import random
import pytest
from bs4 import BeautifulSoup as bs4
import requests
from mc_webscrapper.scrapper_dataclass import ScrapperDataClass
from mc_webscrapper.locobox.locobox_links import LINKS
from mc_webscrapper.locobox.locobox import LocoBox


LINK = ("https://locobox.pl/pl/p/Szafa-aktowa-PROFI-O100200-RODO/546", "SBM 203")
HTML = requests.get(LINK[0])
SOUP = bs4(HTML.text, 'html.parser')
lb = LocoBox()

def test_LINKS():
    link = random.choice(LINKS)
    assert link

def test_setup_scrapper():
    if SOUP:
        assert isinstance(SOUP, bs4)

def test_gather_data_from_link_dataclass():
    b = ScrapperDataClass(name="Locobox")
    assert isinstance(b, ScrapperDataClass)

def test_dealer_name():
    assert lb.get_dealer_name() == "Locobox"

def test_get_manufacturer_name():
    assert lb.get_manufacturer_name() == "Locobox"

def test_get_model_name():
    model = lb.get_model_name(SOUP).lower()
    assert model == "Szafa aktowa PROFI O100/200 RODO".lower()

def test_get_shop_price_nett():
    price_nett = lb.get_shop_price_nett(SOUP)
    assert price_nett == int(1065)

def test_get_product_height():
    height = lb.get_product_height(SOUP)
    assert height == 1990

def test_get_product_width():
    width = lb.get_product_width(SOUP)
    assert width == 1000

def test_get_product_depth():
    depth = lb.get_product_depth(SOUP)
    assert depth == 435

def test_get_product_features():
    features = lb.get_product_features(SOUP)
    assert (features != "") and features is not None

def test_get_lead_time():
    lead_time = lb.get_lead_time(SOUP)
    assert lead_time == "3-4 tygodnie"

def test_get_product_warranty():
    assert lb.get_product_warranty() == 2

@pytest.mark.skip()
def test_get_comment():
    pass

def test_save():
    assert lb.save()

def test_run():
    assert isinstance(lb.run(), list)
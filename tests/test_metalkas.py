import random
import pytest
from bs4 import BeautifulSoup as bs4
import requests
from mc_webscrapper.scrapper_dataclass import ScrapperDataClass
from mc_webscrapper.metalkas.metalkas_links import LINKS
from mc_webscrapper.metalkas.metalkas import Metalkas


LINK = ("https://sklep.metalkas.com.pl/szafy-schowkowe-metalowe-tg-4mss-eco.html", "SBM 203")
HTML = requests.get(LINK[0])
SOUP = bs4(HTML.text, 'html.parser')
mk = Metalkas()

def test_LINKS():
    link = random.choice(LINKS)
    assert link

def test_setup_scrapper():
    if SOUP:
        assert isinstance(SOUP, bs4)

def test_gather_data_from_link_dataclass():
    b = ScrapperDataClass(name="Metalkas")
    assert isinstance(b, ScrapperDataClass)

def test_dealer_name():
    assert mk.get_dealer_name() == "Metalkas"

def test_get_manufacturer_name():
    assert mk.get_manufacturer_name() == "Metalkas"

def test_get_model_name():
    model = mk.get_model_name(SOUP).lower()
    assert model == "Szafy schowkowe metalowe TG-4MSS-ECO".lower()

def test_get_shop_price_nett():
    price_nett = mk.get_shop_price_nett(SOUP)
    assert price_nett == int(997 / 1.3)

def test_get_product_height():
    height = mk.get_product_height(SOUP)
    assert height == 1800

def test_get_product_width():
    width = mk.get_product_width(SOUP)
    assert width == 600

def test_get_product_depth():
    depth = mk.get_product_depth(SOUP)
    assert depth == 490

def test_get_product_features():
    features = mk.get_product_features(SOUP)
    assert (features != "") and features is not None

def test_get_lead_time():
    lead_time = mk.get_lead_time(SOUP)
    assert lead_time == "WYSYŁKA DO 24H"

def test_get_product_warranty():
    assert mk.get_product_warranty() == 2

@pytest.mark.skip()
def test_get_comment():
    pass

def test_save():
    assert mk.save()

def test_run():
    assert isinstance(mk.run(), list)
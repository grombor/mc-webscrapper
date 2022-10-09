import random
import pytest
from bs4 import BeautifulSoup as bs4
import requests
from mc_webscrapper.scrapper_dataclass import ScrapperDataClass
from mc_webscrapper.jan_nowak.jannowak_links import LINKS
from mc_webscrapper.jan_nowak.jannowak import JanNowak


LINK = ("https://jannowak.com/119-szafa-metalowa-kacper-ii-szara-socjalna", "SUM 320")
HTML = requests.get(LINK[0])
SOUP = bs4(HTML.text, 'html.parser')
jn = JanNowak()

def test_LINKS():
    link = random.choice(LINKS)
    assert link

def test_setup_scrapper():
    if SOUP:
        assert isinstance(SOUP, bs4)

def test_gather_data_from_link_dataclass():
    b = ScrapperDataClass(name="Jan Nowak")
    assert isinstance(b, ScrapperDataClass)

def test_dealer_name():
    assert jn.get_dealer_name() == "Jan Nowak"

def test_get_manufacturer_name():
    assert jn.get_manufacturer_name() == "Jan Nowak"

def test_get_model_name():
    model = jn.get_model_name(SOUP).lower()
    assert model == "KACPER-II-szara".lower()

def test_get_shop_price_nett():
    price_nett = jn.get_shop_price_nett(SOUP)
    assert price_nett == int(997/1.23)

def test_get_product_height():
    height = jn.get_product_height(SOUP)
    assert height == 1800

def test_get_product_width():
    width = jn.get_product_width(SOUP)
    assert width == 600

def test_get_product_depth():
    depth = jn.get_product_depth(SOUP)
    assert depth == 500

def test_get_product_features():
    features = jn.get_product_features(SOUP)
    assert (features != "") and features is not None

def test_get_lead_time():
    lead_time = jn.get_lead_time(SOUP)
    assert lead_time == "24h (w dni robocze)"

def test_get_product_warranty():
    assert jn.get_product_warranty() == 24

def test_get_comment():
    comment = "Firma posiada w swojej ofercie meble wymagające samodzielnego montażu."
    assert jn.get_comment() == comment

def test_save():
    assert jn.save()

def test_run():
    assert isinstance(jn.run(), list)
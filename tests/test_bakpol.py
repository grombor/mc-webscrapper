import random
import pytest
from bs4 import BeautifulSoup as bs4
import requests
from mc_webscrapper.scrapper_dataclass import ScrapperDataClass
from mc_webscrapper.bakpol.bakpol_links import LINKS
from mc_webscrapper.bakpol.bakpol import Bakpol


LINK = ("https://bakpol.pl/szafy-biurowe-wysokie/698-sb1000-4-szafa-biurowa.html", "SBM 203")
HTML = requests.get(LINK[0])
SOUP = bs4(HTML.text, 'html.parser')
bakpol = Bakpol()

def test_LINKS():
    link = random.choice(LINKS)
    assert link

def test_setup_scrapper():
    if SOUP:
        assert isinstance(SOUP, bs4)

def test_gather_data_from_link_dataclass():
    b = ScrapperDataClass(name="Bakpol")
    assert isinstance(b, ScrapperDataClass)

def test_dealer_name():
    assert bakpol.get_dealer_name() == "Bakpol"

def test_get_manufacturer_name():
    assert bakpol.get_manufacturer_name() == "Bakpol"

def test_get_model_name():
    model = bakpol.get_model_name(SOUP).lower()
    assert model == "SB1000/4 SZAFA BIUROWA".lower()

def test_get_shop_price_nett():
    price_nett = bakpol.get_shop_price_nett(SOUP)
    assert price_nett == 1788

def test_get_product_height():
    height = bakpol.get_product_height(SOUP)
    assert height == 1950

def test_get_product_width():
    width = bakpol.get_product_width(SOUP)
    assert width == 1000

def test_get_product_depth():
    depth = bakpol.get_product_depth(SOUP)
    assert depth == 400

def test_get_product_features():
    features = bakpol.get_product_features(SOUP)
    assert (features != "") and features is not None

def test_get_lead_time():
    lead_time = bakpol.get_lead_time()
    assert lead_time == ""

def test_get_product_warranty():
    assert bakpol.get_product_warranty() == 2

def test_get_comment():
    assert bakpol.get_comment() == ""

def test_save():
    assert bakpol.save()

def test_run():
    assert isinstance(bakpol.run(), list)
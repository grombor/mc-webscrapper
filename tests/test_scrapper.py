import pytest
from src.mc_webscrapper.scrapper_dataclass import ScrapperDataClass, get_current_month, get_current_year

STRING_TESTING: str = "#$KF"
MONTH_TESTING: int = "07"
YEAR_TESTING = "2022"
INT_TESTING = 999



@pytest.fixture
def scrapper():
    s = ScrapperDataClass(name="test")
    return s


def test_scrapper_name(scrapper):
    assert scrapper.name == "test"


def test_scrapper_dealer(scrapper):
    scrapper.dealer = STRING_TESTING
    assert scrapper.dealer == STRING_TESTING


def test_scrapper_manufacturer(scrapper):
    scrapper.manufacturer = STRING_TESTING
    assert scrapper.manufacturer == STRING_TESTING


def test_scrapper_current_month_of_year(scrapper):
    scrapper.month_of_year = get_current_month()
    assert scrapper.month_of_year == MONTH_TESTING


def test_scrapper_current_year(scrapper):
    scrapper.month_of_year = get_current_year()
    assert scrapper.month_of_year == YEAR_TESTING


def test_scrapper_model(scrapper):
    scrapper.model = STRING_TESTING
    assert scrapper.model == STRING_TESTING


def test_scrapper_substitute(scrapper):
    scrapper.substitute = STRING_TESTING
    assert scrapper.substitute == STRING_TESTING


def test_scrapper_catalogue_price_nett(scrapper):
    scrapper.catalogue_price_nett = INT_TESTING
    assert scrapper.catalogue_price_nett == INT_TESTING


def test_scrapper_shop_price_nett(scrapper):
    scrapper.shop_price_nett = INT_TESTING
    assert scrapper.shop_price_nett == INT_TESTING


def test_scrapper_product_height(scrapper):
    scrapper.product_height = INT_TESTING
    assert scrapper.product_height == INT_TESTING


def test_scrapper_product_width(scrapper):
    scrapper.product_width = INT_TESTING
    assert scrapper.product_width == INT_TESTING


def test_scrapper_product_depth(scrapper):
    scrapper.product_depth = INT_TESTING
    assert scrapper.product_depth == INT_TESTING


def test_scrapper_product_features(scrapper):
    scrapper.product_features = STRING_TESTING
    assert scrapper.product_features == STRING_TESTING


def test_scrapper_product_card_link(scrapper):
    scrapper.product_card_link = STRING_TESTING
    assert scrapper.product_card_link == STRING_TESTING


def test_scrapper_lead_time(scrapper):
    scrapper.lead_time = INT_TESTING
    assert scrapper.lead_time == INT_TESTING


def test_scrapper_product_warranty(scrapper):
    scrapper.product_warranty = INT_TESTING
    assert scrapper.product_warranty == INT_TESTING


def test_scrapper_comment(scrapper):
    scrapper.comment = STRING_TESTING
    assert scrapper.comment == STRING_TESTING
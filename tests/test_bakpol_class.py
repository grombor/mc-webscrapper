import pytest
from src.mc_webscrapper.bakpol import Bakpol


# class TestClass:

@pytest.fixture
def bakpol():
    return Bakpol()


def test_get_list_is_list(bakpol):
    """ Check is get_list returns a list"""

    assert type(bakpol.get_links()) == list


def test_get_list_is_list(bakpol):
    """ Check is get_list items is a tuple"""

    assert type(bakpol.get_links()[0]) == tuple


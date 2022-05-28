import pytest
from src.mc_webscrapper.bakpol import Bakpol
from src.mc_webscrapper.bakpol_links import links
from src.mc_webscrapper.utils import write_to_csv_file, records
from bs4 import BeautifulSoup as bs4
import requests
from random import randint


# class TestClass:

@pytest.fixture
def bakpol():
    return Bakpol()


def test_get_list_is_list(bakpol):
    """ Check is get_list returns a list"""

    assert type(bakpol.get_links()) == list


def test_get_list_is_tuple(bakpol):
    """ Check is get_list items is a tuple"""

    assert type(bakpol.get_links()[0]) == tuple


def test_get_model(bakpol):
    """ Checks output is a string type."""

    # Get url
    index = randint(0, len(links))
    link = links[index]
    # Use requests to retrieve data from a given URL
    url = link[0]
    response = requests.get(url)

    # Parse the whole HTML page using BeautifulSoup
    soup = bs4(response.text, 'html.parser')

    assert type(bakpol.get_model(url, soup)) == str


def test_random_link(bakpol):
    """ Takes random links and run it. """

    # Calculate how much is 10% of links
    percent = 10
    sample_links_range = int(len(links)/percent)
    print(sample_links_range)

    # Create list of samples
    test_link_list = list()
    for i in range(sample_links_range):
        test_link_list.append(links[i])

    for link in test_link_list:
        bakpol.scrap_link(link)

    write_to_csv_file(test=True)

    assert len(records) > 0

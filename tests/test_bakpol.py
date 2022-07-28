import pytest
from src.mc_webscrapper.scrapper import Scrapper
from src.mc_webscrapper.bakpol.bakpol_links import links

def test_bakpol_name():
    bakpol = Scrapper(name="Bakpol")
    assert bakpol.name == "Bakpol"


def test_get_links():
    assert len(links) > 0
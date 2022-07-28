# TODOS:
# add dataclass to csv feature https://pypi.org/project/dataclass-csv/



from dataclasses import dataclass
from datetime import datetime

from attr import field


def get_current_month():
    return datetime.now().month


def get_current_year():
    return datetime.now().year


@dataclass
class Scrapper:
    name: str
    dealer: str = field(init=False)                     # Dystrybutor
    manufacturer: str = field(init=False)               # Producent
    month_of_year: int = get_current_month()            # Miesiąc
    year: int = get_current_year()                      # Rok
    model: str = field(init=False)                      # Model
    substitute: str = field(init=False)                 # Odpowiednik
    catalogue_price_nett: int = field(init=False)       # Cena katalogowa netto [PLN]
    shop_price_nett: int = field(init=False)            # Cena sklepu internetowego netto [PLN]
    product_height: int = field(init=False)             # Wysokość
    product_width: int = field(init=False)              # Szerokość
    product_depth: int = field(init=False)              # Głębokość
    product_features: int = field(init=False)           # Cechy charakterystyczne
    product_card_link: str = field(init=False)          # Link do sklepu
    lead_time: int = field(init=False)                  # Czas realizacji [dni]
    product_warranty: int = field(init=False)           # Gwarancja [lata]
    comment: str = field(init=False)                    # Komentarz

    




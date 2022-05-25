from src.mc_webscrapper.bakpol import Bakpol
from src.mc_webscrapper.utils import write_to_csv_file

bakpol = Bakpol()
bakpol.scrap()
write_to_csv_file()
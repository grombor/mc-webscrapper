from src.mc_webscrapper.metalkas import Metalkas
from src.mc_webscrapper.utils import write_to_csv_file

bakpol = Metalkas()
bakpol.scrap()
write_to_csv_file()
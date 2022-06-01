from src.mc_webscrapper.bakpol import Bakpol
from src.mc_webscrapper.jannowak import JanNowak
from src.mc_webscrapper.kartmap import KartMap
from src.mc_webscrapper.locobox import Locobox
from src.mc_webscrapper.metalkas import Metalkas

from src.mc_webscrapper.utils import write_to_csv_file

bakpol = Bakpol() #done, but still need to do tests
bakpol.scrap()
# jannowak = JanNowak() # need price tests
# jannowak.scrap()
# kartmap = KartMap() # need price tests
# kartmap.scrap()
# locobox = Locobox()
# locobox.scrap()
# metalkas = Metalkas()
# metalkas.scrap()

write_to_csv_file()


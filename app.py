# from mc_webscrapper.bakpol import Bakpol
# from mc_webscrapper.jannowak import JanNowak
# from mc_webscrapper.kartmap import KartMap
# from mc_webscrapper.locobox import Locobox
# from mc_webscrapper.metalkas import Metalkas

# from mc_webscrapper.utils import write_to_csv_file

# bakpol = Bakpol()
# bakpol.scrap()
# write_to_csv_file("bakpol")
# print(help(Bakpol()))
# print(dir(Bakpol()))


# jannowak = JanNowak()
# jannowak.scrap()
# write_to_csv_file("jannowak")

# kartmap = KartMap()
# kartmap.scrap()
# write_to_csv_file("kartmap")

# locobox = Locobox()
# locobox.scrap()
# write_to_csv_file("locobox")

# metalkas = Metalkas()
# metalkas.scrap()
# write_to_csv_file("metalkas")

from mc_webscrapper.bakpol.bakpol import Bakpol
from mc_webscrapper.jan_nowak.jannowak import JanNowak
from mc_webscrapper.kartmap.kartmap import KartMap


def main():
    # bakpol = Bakpol()
    # bakpol.run()
    # jan_nowak = JanNowak()
    # jan_nowak.run()
    kart_map = KartMap()
    kart_map.run()

if __name__ == "__main__":
    main()

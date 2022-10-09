from mc_webscrapper.bakpol.bakpol import Bakpol
from mc_webscrapper.jan_nowak.jannowak import JanNowak
from mc_webscrapper.kartmap.kartmap import KartMap
from mc_webscrapper.locobox.locobox import LocoBox
from mc_webscrapper.metalkas.metalkas import Metalkas
from mc_webscrapper.umstahl.umstahl import Umstahl


def main():
    Bakpol().run()
    JanNowak().run()
    KartMap().run()
    LocoBox().run()
    Metalkas().run()
    Umstahl().run()

if __name__ == "__main__":
    main()

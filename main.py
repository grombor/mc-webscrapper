from modules.km import get_results as Kartmap
from modules.lb import get_results as Locobox
from modules.bp import get_results as Bakpol
from modules.mk import get_results as Metalkas
from modules.us import get_results as Umstahl
from modules.jn import get_results as JanNowak
from modules.utils import *

if __name__ == "__main__":
    Kartmap()
    Locobox()
    Bakpol()
    Metalkas()
    Umstahl()
    JanNowak()
    
    write_to_csv_file()
    
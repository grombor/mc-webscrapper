from modules.km import get_results as Kartmap
from modules.lb import get_results as Locobox
from modules.mk import get_results as Metalkas
from modules.us import get_results as Umstahl
from modules.utils import *




if __name__ == "__main__":
    Kartmap()
    Metalkas()
    Umstahl()
    Locobox()
    test_write_csv_file()
    
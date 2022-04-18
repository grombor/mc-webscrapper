from modules.lb import print_result as Locobox
from modules.mk import print_result as Metalkas, get_results
from modules.us import print_result as Umstahl
from modules.utils import *




if __name__ == "__main__":
    Metalkas()
    # Umstahl()
    # Locobox()
    test_write_csv_file(get_results())
    
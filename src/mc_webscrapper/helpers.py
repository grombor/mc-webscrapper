import sys


def show_status(item, set):
    for i in range(len(set)):
        sys.stdout.write(f"Progress: {item} of {len(set)} \r")
        sys.stdout.flush()

def clear_price(nett_price: str) -> int:
    nett_price = nett_price.split(",")[0]
    return int(''.join([i for i in nett_price if i.isdigit()]))

def extract_digits(string: str) -> int:
    return int(''.join([i for i in string if i.isdigit()]))
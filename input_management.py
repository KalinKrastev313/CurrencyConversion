from constants import currency_codes
from datetime import datetime

from custom_exceptions import ProgramEndedException, DateInWrongFormat


def receive_input():
    result = input().strip()
    if not result.upper() == "END":
        return result
    else:
        raise ProgramEndedException


def receive_amount_and_validate():
    while True:
        amount = receive_input()
        try:
            value = float(amount)

            if round(value, 2) == value:
                return value
            else:
                print("Please enter a valid amount")
        except ValueError:
            print("Please enter a valid amount")


def receive_currency_and_validate():
    while True:
        curr_code = receive_input()
        # The first check for length is executed first and thus saves time
        if len(curr_code) == 3 and curr_code.upper() in currency_codes:
            return curr_code.upper()
        else:
            print('Please enter a valid currency code')


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        raise DateInWrongFormat

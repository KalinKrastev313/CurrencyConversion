import sys
from datetime import datetime

from constants import currency_codes


def receive_amount_and_validate():
    while True:
        amount = input()
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
        curr_code = input()
        # The first check for length is executed first and thus saves time
        if len(curr_code) == 3 and curr_code.upper() in currency_codes:
            return curr_code.upper()
        else:
            print('Please enter a valid currency code')


def main(date_str):
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        print(f"Performing currency conversion for the date: {date.strftime('%Y-%m-%d')}")

        amount = receive_amount_and_validate()
        base_currency = receive_currency_and_validate()
        target_currency = receive_currency_and_validate()

        print(base_currency)
        print(target_currency)
    except ValueError:
        print("Error: The date format should be YYYY-MM-DD.")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 CurrencyConversion.py YYYY-MM-DD")
        sys.exit(1)

    date_str = sys.argv[1]
    main(date_str)
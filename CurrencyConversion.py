import sys
from datetime import datetime
import requests
import json

from constants import currency_codes
from custom_exceptions import ProgramEndedException

with open('config.json', 'r') as file:
    api_key = json.load(file)['api_key']


def receive_input():
    result = input()
    if not result.upper() == "END":
        return result
    else:
        raise ProgramEndedException


def calculate_result(amount, base_currency, target_currency, conversion_rate):
    return f"{amount:.2f} {base_currency} is {(amount * conversion_rate):.2f} {target_currency}"


def get_conversion_rate_from_api(base_currency, target_currency, date):
    url = f"https://api.fastforex.io/historical?api_key={api_key}&from={base_currency}&to={target_currency}&date={date}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if 'results' in data:
            return data['results'][target_currency]
        # Error yet to be handled
    else:
        return {'error': f"Error {response.status_code}: {response.text}"}


def get_cached_conversion_rate(base_currency, target_currency):
    return None


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


def main(date_str):
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        print(f"Performing currency conversion for the date: {date.strftime('%Y-%m-%d')}")

        amount = receive_amount_and_validate()
        base_currency = receive_currency_and_validate()
        target_currency = receive_currency_and_validate()

        cached_conversion_rate = get_cached_conversion_rate(base_currency, target_currency)
        conversion_rate = cached_conversion_rate if cached_conversion_rate else get_conversion_rate_from_api(base_currency, target_currency, date)

        print(calculate_result(amount, base_currency, target_currency, conversion_rate))
    except ValueError:
        print("Error: The date format should be YYYY-MM-DD.")
        sys.exit(1)
    except ProgramEndedException:
        print("Program was ended")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 CurrencyConversion.py YYYY-MM-DD")
        sys.exit(1)

    date_str = sys.argv[1]
    main(date_str)
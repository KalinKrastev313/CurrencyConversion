import os
import sys
from datetime import datetime
import requests
import json

from constants import currency_codes
from custom_exceptions import ProgramEndedException, DateInWrongFormat, FormattingInputException

with open('config.json', 'r') as file:
    api_key = json.load(file)['api_key']


def receive_input():
    result = input()
    if not result.upper() == "END":
        return result
    else:
        raise ProgramEndedException


def calculate_converted_amount(amount, conversion_rate):
    return amount * conversion_rate


def output_result(amount, base_currency, target_currency, converted_amount):
    print(f"{amount:.2f} {base_currency} is {converted_amount:.2f} {target_currency}")


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


def parse_date(date_str):
    try:
        return datetime.strptime(date_str, '%Y-%m-%d')
    except ValueError:
        raise DateInWrongFormat


def create_conversion_entry(date_str, amount, base_currency, target_currency, converted_amount):
    return [
        {
            "date": date_str,
            "amount": amount,
            "base_currency": base_currency,
            "target_currency": target_currency,
            "converted_amount": converted_amount
        }
            ]


def load_json_file_if_exists_or_return_empty_list(filepath):
    if os.path.exists(filepath):
        with open(filepath, 'r') as file:
            try:
                data = json.load(file)
            except json.JSONDecodeError:
                data = []
        return data
    return []


def update_json_file(filepath, new_entry):
    data = load_json_file_if_exists_or_return_empty_list(filepath)
    data.append(new_entry)

    # Some sources claim that due to json structure, append from the last line wouldn't work and thus rewriting is standard
    with open(filepath, 'w') as file:
        json.dump(data, file, indent=4)


def save_conversion_rates(date_str, base_currency, target_currency, conversion_rate):
    data = load_json_file_if_exists_or_return_empty_list('cached_conversion_rates.json')


    # conversion_rates = {
    #     "USD": {"EUR": 0.85, "JPY": 110.53, "GBP": 0.75},
    #     "EUR": {"USD": 1.18, "JPY": 130.02, "GBP": 0.88}
    # }

    def update_nested_dict(d, keys, value):
        for key in keys[:-1]:
            if key not in d:
                d[key] = {}
            d = d[key]
        d[keys[-1]] = value
    if data == []:
        cache_dict = {}
        data = [cache_dict]
    else:
        cache_dict = data[0]

    update_nested_dict(cache_dict, [date_str, base_currency, target_currency], conversion_rate)

    with open('cached_conversion_rates.json', 'w') as file:
        json.dump(data, file, indent=4)


def main(date_str):
    try:
        date = parse_date(date_str)
        print(f"Performing currency conversion for the date: {date.strftime('%Y-%m-%d')}")

        amount = receive_amount_and_validate()
        base_currency = receive_currency_and_validate()
        target_currency = receive_currency_and_validate()

        cached_conversion_rate = get_cached_conversion_rate(base_currency, target_currency)
        conversion_rate = cached_conversion_rate if cached_conversion_rate else get_conversion_rate_from_api(base_currency, target_currency, date)

        print(conversion_rate)
        converted_amount = calculate_converted_amount(amount, conversion_rate)
        output_result(amount, base_currency, target_currency, converted_amount)

        new_entry = create_conversion_entry(date_str, amount, base_currency, target_currency, converted_amount)
        update_json_file('conversions.json', new_entry)

        save_conversion_rates(date_str, base_currency, target_currency, conversion_rate)

    # except ValueError:
    #     print("Error: The date format should be YYYY-MM-DD.")
    #     sys.exit(1)
    except FormattingInputException as e:
        print(e.correct_format_message)
        if e.should_finish_program:
            sys.exit(1)
    except ProgramEndedException:
        print("Program was ended")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 CurrencyConversion.py YYYY-MM-DD")
        sys.exit(1)

    date_str = sys.argv[1]
    main(date_str)
import requests
from json_cache_and_logs_management import get_api_key_from_config
from custom_exceptions import APIResponseError


def calculate_converted_amount(amount, conversion_rate):
    return amount * conversion_rate


def output_result(amount, base_currency, target_currency, converted_amount):
    print(f"{amount:.2f} {base_currency} is {converted_amount:.2f} {target_currency}")


def get_conversion_rate_from_api(base_currency, target_currency, date):
    api_key = get_api_key_from_config()
    url = f"https://api.fastforex.io/historical?api_key={api_key}&from={base_currency}&to={target_currency}&date={date}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        if 'results' in data:
            return data['results'][target_currency]
    else:
        raise APIResponseError(response)

import os
import json


class JSONManager:
    @staticmethod
    def load_json_file_if_exists_or_return_empty_list(filepath):
        if os.path.exists(filepath):
            with open(filepath, 'r') as file:
                try:
                    data = json.load(file)
                except json.JSONDecodeError:
                    data = []
            return data
        return []

    @staticmethod
    def rewrite_the_data_into_a_json_file(filepath, data):
        # Some sources claim that due to json structure, append from the last line wouldn't work and thus rewriting is standard
        with open(filepath, 'w') as file:
            json.dump(data, file, indent=4)

    @staticmethod
    def update_nested_dict(d, keys, value):
        for key in keys[:-1]:
            if key not in d:
                d[key] = {}
            d = d[key]
        d[keys[-1]] = value


class ConversionsLogsController(JSONManager):
    LOGS_DIRECTORY = 'conversions.json'

    def __init__(self, date_str, amount, base_currency, target_currency, converted_amount):
        self.date_str = date_str
        self.amount = amount
        self.base_currency = base_currency
        self.target_currency = target_currency
        self.converted_amount = converted_amount

    def _create_conversion_entry(self):
        return {
            "date": self.date_str,
            "amount": self.amount,
            "base_currency": self.base_currency,
            "target_currency": self.target_currency,
            "converted_amount": self.converted_amount
        }

    def update_logs(self):
        data = self.load_json_file_if_exists_or_return_empty_list(self.LOGS_DIRECTORY)
        data.append(self._create_conversion_entry())

        self.rewrite_the_data_into_a_json_file(self.LOGS_DIRECTORY, data)


class ConversionsCacheController(JSONManager):
    CACHE_DIRECTORY = 'cached_conversion_rates.json'

    def __init__(self, date_str, base_currency, target_currency):
        self.date_str = date_str
        self.base_currency = base_currency
        self.target_currency = target_currency

    def save_conversion_rates(self, conversion_rate):
        data = self.load_json_file_if_exists_or_return_empty_list(self.CACHE_DIRECTORY)

        if data == []:
            cache_dict = {}
            data = [cache_dict]
        else:
            cache_dict = data[0]

        self.update_nested_dict(cache_dict, [self.date_str, self.base_currency, self.target_currency], conversion_rate)

        self.rewrite_the_data_into_a_json_file(self.CACHE_DIRECTORY, data)

    def get_cached_conversion_rate(self):
        with open(self.CACHE_DIRECTORY, 'r') as file:
            data = json.load(file)[0]

        if self.date_str in data and self.base_currency in data[self.date_str] and self.target_currency in data[self.date_str][self.base_currency]:
            return data[self.date_str][self.base_currency][self.target_currency]
        return None


def get_api_key_from_config():
    with open('config.json', 'r') as file:
        api_key = json.load(file)['api_key']
    return api_key
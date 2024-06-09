import sys
from misc_functions import get_conversion_rate_from_api, calculate_converted_amount, output_result
from input_management import parse_date, receive_amount_and_validate, receive_currency_and_validate
from custom_exceptions import CustomException
from json_cache_and_logs_management import ConversionsCacheController, ConversionsLogsController


def main(date_str):
    while True:
        try:
            date = parse_date(date_str)
            print(f"Performing currency conversion for the date: {date.strftime('%Y-%m-%d')}")

            amount = receive_amount_and_validate()
            base_currency = receive_currency_and_validate()
            target_currency = receive_currency_and_validate()

            cache_manager = ConversionsCacheController(date_str, base_currency, target_currency)
            cached_conversion_rate = cache_manager.get_cached_conversion_rate()
            conversion_rate = cached_conversion_rate if cached_conversion_rate else get_conversion_rate_from_api(base_currency, target_currency, date)
            cache_manager.save_conversion_rates(conversion_rate)

            converted_amount = calculate_converted_amount(amount, conversion_rate)
            output_result(amount, base_currency, target_currency, converted_amount)

            logs_manager = ConversionsLogsController(date_str, amount, base_currency, target_currency, converted_amount)
            logs_manager.update_logs()

        # These can be extended or somehow merged
        except CustomException as e:
            print(e.error_message)
            if e.should_finish_program:
                sys.exit(1)
            break


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 CurrencyConversion.py YYYY-MM-DD")
        sys.exit(1)

    date_str = sys.argv[1]
    main(date_str)

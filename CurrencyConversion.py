import sys
from datetime import datetime


def main(date_str):
    try:
        date = datetime.strptime(date_str, '%Y-%m-%d')
        print(f"Performing currency conversion for the date: {date.strftime('%Y-%m-%d')}")

        print("Currency conversion logic goes here.")

    except ValueError:
        print("Error: The date format should be YYYY-MM-DD.")
        sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 CurrencyConversion.py YYYY-MM-DD")
        sys.exit(1)

    date_str = sys.argv[1]
    main(date_str)
import logging

# logging.basicConfig(filename='transaction_log.txt', level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Set up logging
# logging.basicConfig(level=logging.DEBUG)


class Sorts:
    dateSort = 1
    descSort = 2
    amountSort = 3


def parseCurrency(value):
    try:
        value = value.replace('£', '').replace(',', '').strip()
        return float(value) if value else 0.0
    except ValueError:
        # static.logging.error(f"Error parsing currency value: '{value}'")
        return 0.0

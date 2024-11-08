from decimal import Decimal, InvalidOperation
import logging


def extract_city_from_location(location: str, cities: list) -> str:
    """
    Extract the first city name from a location string using a list of cities.

    Return 'Unknown' if no city is found.
    """
    for city in cities:
        if city in location:
            return city
    return "Unknown"


def parse_decimal(value):
    """
    Extract the city name from a location string using a list of cities.

    Args:
        location (str): The location string to search for a city name.
        cities (list): A list of city names to search within the location.

    Returns:
        str: The name of the city found, or "Unknown" if no city is found.
    """
    value = value.replace(" ", "").replace("Ft", "")
    value = "".join(filter(lambda x: x.isdigit() or x == ".", value))
    try:
        return Decimal(value) if value else None
    except InvalidOperation:
        logging.error(f"Invalid decimal value: {value}")
        return None


def parse_int(value):
    """
    Extract digits from the input string and return them as an integer.

    Args:
        value (str): The input string to parse.

    Returns:
        int or None: An integer composed of all digits in the input string,
        or None if no digits are found.
    """
    value = "".join(filter(str.isdigit, value))
    return int(value) if value else None

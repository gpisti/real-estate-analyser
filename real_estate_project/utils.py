from decimal import Decimal, InvalidOperation
import logging
import re


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
    value = re.sub(r"[^\d.]", "", value.replace("Ft", "").strip())
    try:
        return Decimal(value) if value else None
    except InvalidOperation:
        logging.error(f"Invalid decimal value: {value}")
        return None


def parse_int(value):
    """
    Parse a numeric value from a string and return it as a Decimal.

    Removes spaces and currency symbols, then filters digits and the decimal point.
    Returns None if the value cannot be parsed.

    Args:
        value (str): The input string to parse.

    Returns:
        Decimal or None: A decimal representation of the value or None if invalid.
    """
    digits = re.sub(r"\D", "", value)
    return int(digits) if digits else None

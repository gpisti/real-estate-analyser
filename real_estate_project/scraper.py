import os
import sys
import csv
import requests
from bs4 import BeautifulSoup
from utils import extract_city_from_location
import internal_logging as logging

sys.stdout.reconfigure(encoding="utf-8")


def load_cities_from_csv(file_path: str) -> list:
    """
    Load a list of cities from a CSV file.

    Args:
        file_path (str): The path to the CSV file containing city names.

    Returns:
        list: A list of city names extracted from the CSV file.
    """
    city_list = []
    try:
        relative_path = os.path.join(os.path.dirname(__file__), file_path)
        with open(relative_path, "r", encoding="utf8") as file:
            reader = csv.reader(file)
            header = next(reader, None)
            if header and "city" in header:
                city_index = header.index("city")
            else:
                city_index = 0

            for row in reader:
                if row and row[city_index]:
                    city_list.append(row[city_index].strip())
        logging.info(f"Loaded {len(city_list)} cities from the CSV file.")
    except FileNotFoundError as e:
        logging.error(f"CSV file not found: {e}")
    except Exception as e:
        logging.error(f"Error loading cities from CSV: {e}")
    return city_list


def fetch_page_content(url: str) -> BeautifulSoup:
    """
    Fetch the page content from the given URL and return a BeautifulSoup object.

    Args:
        url (str): The URL of the page to fetch.

    Returns:
        BeautifulSoup or None: A BeautifulSoup object of the parsed HTML content if successful, or None if the request fails.

    Notes:
        Logs an error using internal logging if the page retrieval fails.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        response.encoding = response.apparent_encoding
        return BeautifulSoup(response.text, "html.parser")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to retrieve the page from {url}. Error: {e}")
        return None


def extract_estate_count(soup: BeautifulSoup) -> int:
    """
    Extract the number of available real estate listings from the page content.

    Args:
        soup (BeautifulSoup): Parsed HTML content of the real estate webpage.

    Returns:
        int: Total number of real estate listings found.

    Notes:
        Logs the total count or any extraction errors using the internal logging module.
    """
    try:
        element = soup.select_one("div.col.h5.m-0.fw-bolder")
        count = int(element.text.split()[0]) if element else 0
        logging.info(f"Total real estate listings found: {count}")
        return count
    except Exception as e:
        logging.error(f"Error extracting estate count: {e}")
        return 0


def generate_links(estate_count: int) -> list:
    """
    Generate pagination links based on the total number of listings.

    Args:
        estate_count (int): The total number of estate listings.

    Returns:
        list: A list of pagination URLs.
    """
    max_pages = min(500, estate_count // 20 + 1)
    links = [
        f"https://otthonterkep.hu/elado+minden-kategoria/minden-megye/minden-telepules/0/0/0/0?p={x}&sort=ad_feladas_time%7Cdesc"
        for x in range(1, max_pages + 1)
    ]
    logging.info(f"Generated {len(links)} pagination links.")
    return links


def extract_estate_data(soup: BeautifulSoup, cities: list) -> list:
    """
    Extract real estate data from a BeautifulSoup object using a list of cities.

    Collects property details such as location, price, type, size, rooms, and floor.

    Returns a list of dictionaries containing the property data.

    Logs the number of records extracted.
    """
    data = []
    for estate in range(1, 22):
        temp_location = soup.select_one(
            f"div.properties.slotDoubleColumn > div:nth-child({estate}) h5 > a"
        )
        property_location = extract_city_from_location(
            temp_location.text if temp_location else "", cities
        )
        price = soup.select_one(
            f"div.properties.slotDoubleColumn > div:nth-child({estate}) h4"
        )
        floor = soup.select_one(
            f"div.properties.slotDoubleColumn > div:nth-child({estate}) div:nth-child(2) > div:nth-child(1) > small > span"
        )
        place_size = soup.select_one(
            f"div.properties.slotDoubleColumn > div:nth-child({estate}) div:nth-child(1) > div:nth-child(1) > span"
        )
        land_size = soup.select_one(
            f"div.properties.slotDoubleColumn > div:nth-child({estate}) div:nth-child(1) > div:nth-child(2) > span"
        )
        room_num = soup.select_one(
            f"div.properties.slotDoubleColumn > div:nth-child({estate}) div:nth-child(2) > div:nth-child(1) > small > span"
        )

        if property_location and price and room_num:
            data.append(
                {
                    "property_location": property_location.strip(),
                    "price": price.text.strip(),
                    "type": "House" if room_num.text.strip() == "0" else "Apartment",
                    "place_size": place_size.text.strip() if place_size else "N/A",
                    "land_size": land_size.text.strip() if land_size else "N/A",
                    "rooms": room_num.text.strip() if room_num else "N/A",
                    "floor": floor.text.strip() if floor else "N/A",
                }
            )
    logging.info(f"Extracted {len(data)} real estate records from the page.")
    return data


def scrape_real_estate_data() -> list:
    """
    Scrape real estate data from the website and return it as a list of dictionaries.

    Returns:
        list: A list of dictionaries containing real estate data such as location, price, type, size, rooms, and floor.

    Notes:
        Logs progress and errors during the scraping process using internal logging.
    """
    base_url = "https://otthonterkep.hu/elado+minden-kategoria/minden-megye/minden-telepules/0/0/0/0?p=1&sort=ad_feladas_time%7Cdesc"
    soup = fetch_page_content(base_url)
    if not soup:
        logging.error("Failed to fetch the main page content.")
        return []

    estate_count = extract_estate_count(soup)
    if estate_count == 0:
        logging.error("No real estate listings found.")
        return []

    links = generate_links(estate_count)
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, '..\\turabazis.csv')
    cities = load_cities_from_csv(filename)

    all_data = []
    for link in links:
        page_soup = fetch_page_content(link)
        if page_soup:
            page_data = extract_estate_data(page_soup, cities)
            all_data.extend(page_data)
            logging.info(f"Total records collected so far: {len(all_data)}")
        else:
            logging.warning(f"Skipping link due to fetch error: {link}")
            continue

    logging.info(f"Scraping completed. Total records collected: {len(all_data)}")
    return all_data

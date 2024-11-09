# Real Estate Project

This project is designed to assist in managing and analyzing real estate data. It includes utilities for parsing and extracting information from real estate listings, such as city names and numerical values.

## Features

- **City Extraction**: Extract city names from location strings using a predefined list of cities.
- **Decimal Parsing**: Convert formatted strings into decimal numbers, handling errors gracefully.
- **Integer Parsing**: Extract and convert digits from strings into integers.

## Installation

To use this project, clone the repository and install the required dependencies:

```bash
git clone https://github.com/gisti/real_estate_project.git
cd real_estate_project
pip install -r requirements.txt
```

## Usage
### Extracting City Names
The `extract_city_from_location` function helps to identify the first city name from a location string. It returns "Unknown" if no city is found.

```bash
from real_estate_project.utils import extract_city_from_location

location = "123 Main St, Springfield"
cities = ["Springfield", "Shelbyville", "Ogdenville"]
city = extract_city_from_location(location, cities)
print(city)  # Output: Springfield
```

## Parsing Decimal Values
The `parse_decimal` function converts a string with numerical values into a `Decimal` object. It removes spaces and specific characters like "Ft" before parsing.

```bash
from real_estate_project.utils import parse_decimal

value = "1,234.56 Ft"
decimal_value = parse_decimal(value)
print(decimal_value)  # Output: 1234.56
```

## Parsing Integer Values
The `parse_int` function extracts digits from a string and returns them as an integer.

```bash
from real_estate_project.utils import parse_int

value = "Area: 1500 sqft"
integer_value = parse_int(value)
print(integer_value)  # Output: 1500
```

## Logging
The project uses Python's built-in logging module to report errors, such as invalid decimal values during parsing.

## Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License
This project is licensed under the MIT License. See the LICENSE file for more details.

## Contact
For questions or support, please contact 'galpisti067@gmail.com'.

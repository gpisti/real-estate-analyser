# Real Estate Data Analysis and Visualization

This project is a comprehensive tool for collecting real estate data from [otthonterkep.hu](https://otthonterkep.hu), storing it in an SQL database, and providing data analysis and visualizations through an interactive **Streamlit** web application. Users can refresh the database at any time, apply filters through the user interface, and explore insights derived from the collected data.

## Table of Contents

- [Features](#features)
- [Installation and Setup](#installation-and-setup)
- [Starting the Application](#starting-the-application)
- [Project Structure](#project-structure)
- [Modules and Functions](#modules-and-functions)
  - [app.py](#app.py)
  - [utils.py](#utils.py)
- [Dependencies](#dependencies)
- [Usage Examples](#usage-examples)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Data Collection**: Scrape real estate listings from `otthonterkep.hu`.
- **Database Storage**: Store scraped data in an SQL database for persistent storage and querying.
- **Data Analysis**: Perform analysis to extract insights from the data.
- **Interactive Visualizations**: Generate interactive charts and graphs using **Streamlit** and **Altair**.
- **User Interface**: Interactive UI for data interaction and filtering.
- **Filtering Options**: Apply filters directly through the UI.
- **Database Refresh**: Update the database with new data at any time.

---

## Installation and Setup

### Prerequisites

- **Python 3.7 or higher**: Ensure Python is installed.
- **SQL Database**: Setup an SQL database (e.g., MySQL).

### Clone the Repository

```bash
git clone https://github.com/gpisti/real-estate-analyser.git
cd real_estate_project
```

## Create a Virtual Environment
```bash
python -m venv venv
```

## Activate the virtual environment:

- ### Windows:
```bash
venv\Scripts\activate
```

- ### macOS/Linux:
```bash
source venv/bin/activate
```

## Install Dependencies
```bash
pip install -r requirements.txt
```

## Database Configuration
1. **Install MySQL**: Download from the [official website](https://dev.mysql.com/downloads/installer/).
2. **Create a Database**:
```bash
CREATE DATABASE real_estate_database;
```

3. **Configure Database Settings**: Update the database connection settings in your code (e.g., in `app.py`):
```bash
DATABASE_CONFIG = {
    'user': 'root', #default
    'password': 'root', #default
    'host': 'localhost',
    'database': 'real_estate_database',
}
```
---

## Starting the Application
Run the following command:
```bash
streamlit run app.py
```

Access the application at the URL provided in the console output, typically `http://localhost:8501`.

---

## Project Structure
- `app.py`: Main application script.
- `utils.py`: Utility functions used across the project.
- `requirements.txt`: Python dependencies.
- `README.md`: Project documentation.

```bash
real_estate_project/
├── app.py
├── utils.py
├── scraper.py
├── database.py
├── internal_logging.py
├── analysis.py
├── requirements.txt
└── README.md
```
---

## Modules and Functions
### app.py
The main entry point of the application containing the Streamlit web app logic.

## Core Components:

- Data Scraping: Functions to scrape data from the source website.
- Database Operations: Interact with the SQL database using SQLAlchemy and PyMySQL.
- User Interface: Built with Streamlit for an interactive experience.
- Data Visualization: Generate charts using Altair.
- Data Refresh: Allows users to update the dataset.

### utils.py
Contains utility functions utilized by `app.py` and other modules.

## Functions

1. `extract_city_from_location(location: str, cities: list) -> str`
   
```bash
def extract_city_from_location(location: str, cities: list) -> str:
    """
    Extracts the first city name from a location string using a list of cities.

    Args:
        location (str): The location string to search.
        cities (list): A list of city names.

    Returns:
        str: The name of the city found, or "Unknown" if none is found.
    """
    for city in cities:
        if city in location:
            return city
    return "Unknown"
```

2. `parse_decimal(value: str) -> Decimal`
```bash
def parse_decimal(value: str) -> Decimal:
    """
    Parses a string to extract a decimal number.

    Args:
        value (str): The string containing the decimal value.

    Returns:
        Decimal: The decimal number extracted, or None if invalid.
    """
    value = value.replace(" ", "").replace("Ft", "")
    value = "".join(filter(lambda x: x.isdigit() or x == ".", value))
    try:
        return Decimal(value) if value else None
    except InvalidOperation:
        logging.error(f"Invalid decimal value: {value}")
        return None
```

3. `parse_int(value: str) -> int`
```bash
def parse_int(value: str) -> int:
    """
    Extracts digits from a string and returns them as an integer.

    Args:
        value (str): The input string.

    Returns:
        int: The integer composed of digits found, or None if invalid.
    """
    value = "".join(filter(str.isdigit, value))
    return int(value) if value else None
```

## Dependencies
Ensure all dependencies are installed. Use the internal versions of these libraries if available.

- `streamlit`
- `beautifulsoup4`
- `altair`
- `sqlalchemy`
- `pymysql`
- `pandas`
- `requests`
Install using:
```bash
pip install -r requirements.txt
```
---
## Usage Examples
### Running the Application
Start the application:
```bash
streamlit run app.py
```

### Scraping Data
- Use the "Scrape Data" button in the UI to collect new data.
- Progress will be displayed within the application.
### Viewing and Filtering Data
- Navigate to the "Data Exploration" section.
- Filter data based on criteria like city or price.
### Visualizing Data
- Access the "Data Analysis" section.
- Select analysis types to generate charts.

## License
This project is licensed under the MIT License.

## Contact
For questions, contact the project maintainer at galpisti067@gmail.com.

import pymysql
import pandas as pd
from sqlalchemy import create_engine
from utils import parse_decimal, parse_int
import internal_logging as logging

DB_HOST = "localhost"
DB_USER = "root"
DB_PASSWORD = "root"
DB_NAME = "real_estate_database"


def initialize_database():
    """
    Initialize the database by creating it if it does not exist.

    Connects to the MySQL server using root credentials, checks if the required
    database exists, and creates it if it does not.
    """
    connection = None
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
        )
        logging.info("Connected to the MySQL server as root user.")

        with connection.cursor() as cursor:
            create_db_sql = f"CREATE DATABASE IF NOT EXISTS `{DB_NAME}`;"
            cursor.execute(create_db_sql)
            logging.info(f"Verified that database `{DB_NAME}` exists.")

        connection.commit()
        logging.info("Database initialization completed successfully.")

    except pymysql.MySQLError as e:
        logging.error(f"Error during database initialization: {e}")
        if connection:
            connection.rollback()
    finally:
        if connection:
            connection.close()
            logging.info("MySQL server connection closed.")


def insert_data_into_database(connection, data):
    """
    Insert real estate listings into the database after clearing existing data.

    Creates the 'real_estate_listings' table if it doesn't exist, truncates it,
    processes each record in the provided data by sanitizing and validating fields,
    and then inserts the records into the database.
    """
    try:
        with connection.cursor() as cursor:
            create_table_sql = """
            CREATE TABLE IF NOT EXISTS real_estate_listings (
                id INT AUTO_INCREMENT PRIMARY KEY,
                property_location VARCHAR(255) NOT NULL,
                price DECIMAL(15,2) NOT NULL,
                type VARCHAR(50) NOT NULL,
                place_size DECIMAL(10,2) NOT NULL,
                land_size DECIMAL(10,2),
                rooms INT,
                floor VARCHAR(10)
            );
            """
            cursor.execute(create_table_sql)
            logging.info("Verified that `real_estate_listings` table exists.")

            cursor.execute("TRUNCATE TABLE real_estate_listings;")
            logging.info("Cleared existing data from `real_estate_listings` table.")

            connection.commit()

            insert_sql = """
                INSERT INTO real_estate_listings
                (property_location, price, type, place_size, land_size, rooms, floor)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """

            for record in data:
                property_location = record.get("property_location")
                price = parse_decimal(record.get("price"))
                property_type = record.get("type")
                place_size = parse_decimal(record.get("place_size"))
                land_size = parse_decimal(record.get("land_size", ""))
                rooms = parse_int(record.get("rooms", ""))
                floor = None if record.get("floor") == "N/A" else record.get("floor")

                if any(
                    value is None
                    for value in [property_location, price, property_type, place_size]
                ):
                    logging.warning(
                        f"Skipping record due to missing required fields: {record}"
                    )
                    continue

                try:
                    cursor.execute(
                        insert_sql,
                        (
                            property_location,
                            price,
                            property_type,
                            place_size,
                            land_size,
                            rooms,
                            floor,
                        ),
                    )
                except (pymysql.DataError, pymysql.IntegrityError) as e:
                    logging.error(f"Error when inserting record: {e}")
                    continue
                except Exception as e:
                    logging.error(f"Unexpected error when inserting record: {e}")
                    continue

            connection.commit()
            logging.info("Data inserted into the database successfully.")

    except pymysql.MySQLError as e:
        logging.error(f"Database error: {e}")
        connection.rollback()


def connect_root(data):
    """
    Connect to the database as the root user, initialize the database, and insert data.

    Establishes a connection to the MySQL server as the root user, ensures that the required
    database exists, and then proceeds to insert data into the database.
    """
    initialize_database()
    connection = None
    try:
        connection = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASSWORD,
            database=DB_NAME,
        )
        logging.info("Connected to the database as root user.")
        insert_data_into_database(connection, data)
    except pymysql.MySQLError as e:
        logging.error(f"Error connecting as root user: {e}")
    finally:
        if connection:
            connection.close()
            logging.info("Database connection closed.")


def fetch_data_from_database():
    """
    Fetch data from the `real_estate_listings` table in the database.

    Establishes a connection to the database as the root user and retrieves all records from
    the `real_estate_listings` table as a pandas DataFrame.
    """
    try:
        engine = create_engine(
            f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
        )
        logging.info("Connected to the database as root user.")

        query = "SELECT * FROM real_estate_listings;"

        with engine.connect() as connection:
            df = pd.read_sql(query, connection)
            logging.info(f"Retrieved {len(df)} records from the database.")
            return df

    except Exception as e:
        logging.error(f"Error fetching data from the database: {e}")
        return None

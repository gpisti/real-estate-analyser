import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import internal_logging as logging


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans the input DataFrame by converting data types, handling missing values,
    and resetting the index.

    Parameters:
        df (pd.DataFrame): The input DataFrame containing property data.

    Returns:
        pd.DataFrame: The cleaned DataFrame.
    """
    numeric_columns = ["price", "place_size", "land_size", "rooms", "floor"]
    for col in numeric_columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna(subset=["price", "place_size", "rooms"])

    df = df[(df["price"] >= 5_000_000) & (df["price"] <= 1_000_000_000)]

    df = df.reset_index(drop=True)

    logging.info("Data cleaning completed.")
    return df


def analyze_data(df: pd.DataFrame) -> None:
    """
    Performs data analysis on the DataFrame, including statistical summaries and calculations.

    Parameters:
        df (pd.DataFrame): The DataFrame containing cleaned property data.

    Returns:
        None
    """
    type_counts = df["type"].value_counts()
    logging.info("Property Type Distribution:")
    print(type_counts)

    avg_price_city = (
        df.groupby("property_location")["price"]
        .mean()
        .sort_values(ascending=False)
        .head(10)
    )

    avg_price_city_formatted = avg_price_city.apply(lambda x: f"{x:,.2f}")

    logging.info("Average Price by City:")
    print(avg_price_city_formatted)

    df["price_per_sqm"] = df["price"] / df["place_size"]
    logging.info("Calculated price per square meter.")

    correlation = df[["price", "place_size", "rooms", "price_per_sqm"]].corr()

    logging.info("Correlation Matrix:")
    print(correlation.round(2))


def visualize_data(df: pd.DataFrame) -> None:
    """
    Generates visualizations from the DataFrame, including histograms, bar charts, and heatmaps.

    Parameters:
        df (pd.DataFrame): The DataFrame containing cleaned property data.

    Returns:
        None
    """
    plt.figure(figsize=(10, 6))

    price_upper_limit = df["price"].quantile(0.95)

    sns.histplot(df["price"], bins=50, kde=True)

    plt.title("Distribution of Property Prices", fontsize=16)
    plt.xlabel("Price", fontsize=14)
    plt.ylabel("Number of Properties", fontsize=14)

    plt.xlim(0, price_upper_limit)

    plt.ticklabel_format(style="plain", axis="x")
    plt.tight_layout()
    plt.show()

    top_cities = df.groupby("property_location")["price"].mean().nlargest(10)

    top_cities_formatted = top_cities.apply(lambda x: round(x))

    plt.figure(figsize=(12, 8))
    sns.barplot(x=top_cities_formatted.values, y=top_cities_formatted.index)
    plt.title("Top 10 Cities by Average Property Price", fontsize=16)
    plt.xlabel("Average Price", fontsize=14)
    plt.ylabel("City", fontsize=14)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(8, 6))
    corr_matrix = df[["price", "place_size", "rooms", "price_per_sqm"]].corr()
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f")
    plt.title("Correlation Heatmap", fontsize=16)
    plt.tight_layout()
    plt.show()

    logging.info("Data visualization completed.")
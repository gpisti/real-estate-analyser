import streamlit as st
from scraper import scrape_real_estate_data
from database import fetch_data_from_database, connect_root
from analysis import clean_data
import internal_logging as logging
import altair as alt


@st.cache_data
def load_data():
    """
    Runs the Streamlit application for the Real Estate Listings Dashboard.

    This function initializes and runs the Streamlit app, providing an interactive dashboard
    for real estate data. It allows users to refresh the database by scraping new data,
    filter listings based on various criteria, and view detailed analyses and visualizations
    including key metrics and interactive charts.

    Notes:
        - Provides sidebar options for data filtering and database refreshing.
        - Displays data tables and visualizations using Altair.
        - Logs progress and errors using internal logging.
    """
    return fetch_data_from_database()


def main():
    """
    Runs the Real Estate Listings Dashboard Streamlit application.

    This module initializes and runs a Streamlit app that provides an interactive dashboard
    for real estate data. Users can refresh the database by scraping new data, filter listings
    based on various criteria, and view detailed analyses and visualizations including key
    metrics and interactive charts.

    Features:
    - Provides sidebar options for data filtering and database refreshing.
    - Displays data tables and visualizations using Altair.
    - Utilizes internal modules for data scraping, database interaction, data cleaning, logging, and utilities.

    Notes:
    - Logs progress and errors using internal logging.
    """
    st.title("Real Estate Listings Dashboard")
    logging.info("Starting the real estate data processing application.")

    st.sidebar.header("Options")

    status_text = st.sidebar.empty()

    if st.sidebar.button("Refresh Database and Start Scraping"):
        with st.spinner("Refreshing database and scraping data..."):
            try:
                status_text.text("Scraping data...")
                data = scrape_real_estate_data()
                if not data:
                    st.error("No data scraped. Exiting.")
                    logging.error("No data scraped. Exiting.")
                    status_text.text("Scraping failed.")
                    return
                logging.info(f"Scraped {len(data)} records.")

                status_text.text("Connecting to database...")
                connect_root(data)
                logging.info("Data inserted into the database successfully.")

                status_text.text("Clearing cache and reloading data...")
                load_data.clear()
                st.success("Database refreshed and data reloaded successfully.")
                logging.info("Database refreshed and data reloaded successfully.")
                status_text.text("Process completed successfully.")

            except Exception as e:
                st.error(f"Error refreshing database: {e}")
                logging.error(f"Error refreshing database: {e}")
                status_text.text("Error occurred during process.")
                return

    data_load_state = st.text("Loading data...")
    data = load_data()
    data_load_state.text("")

    if data is None or data.empty:
        st.info(
            "The database is empty. Please populate the database by clicking 'Refresh Database and Start Scraping' in the sidebar."
        )
        logging.error("No data available to display.")
        return

    logging.info("Data fetched for analysis.")

    df_clean = clean_data(data)
    logging.info("Data cleaned for analysis.")

    df_clean["price"] = df_clean["price"].astype(float).round(0).astype(int)

    st.sidebar.subheader("Filter Options")

    city_options = df_clean["property_location"].unique()
    default_city = "Debrecen" if "Debrecen" in city_options else city_options[0]
    selected_city = st.sidebar.selectbox(
        "Select a City",
        options=city_options,
        index=list(city_options).index(default_city),
    )

    st.sidebar.subheader("Property Type")

    either_selected = st.sidebar.checkbox("Either", value=True)

    if either_selected:
        selected_types = df_clean["type"].unique()
    else:
        st.sidebar.write("Select Property Type(s):")
        include_apartment = st.sidebar.checkbox("Apartment")
        include_house = st.sidebar.checkbox("House")
        selected_types = []
        if include_apartment:
            selected_types.append("Apartment")
        if include_house:
            selected_types.append("House")
        if not selected_types:
            selected_types = df_clean["type"].unique()

    min_price = int(df_clean["price"].min())
    max_price = int(df_clean["price"].max())
    price_range = st.sidebar.slider(
        "Select Price Range (Ft)",
        min_value=min_price,
        max_value=max_price,
        value=(min_price, max_price),
        step=500_000,
        format="%d",
    )

    filtered_data = df_clean[
        (df_clean["property_location"] == selected_city)
        & (df_clean["type"].isin(selected_types))
        & (df_clean["price"] >= price_range[0])
        & (df_clean["price"] <= price_range[1])
    ]

    if "id" in filtered_data.columns:
        filtered_data.set_index("id", inplace=True)

    if filtered_data.columns[0] == "Unnamed: 0":
        filtered_data.drop(columns=filtered_data.columns[0], inplace=True)

    st.subheader(f"Real Estate Listings in {selected_city}")
    st.dataframe(filtered_data)

    st.subheader("Data Analysis")

    total_listings = filtered_data.shape[0]
    average_price = filtered_data["price"].mean()
    average_size = filtered_data["place_size"].mean()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Listings", total_listings)
    col2.metric("Average Price (Ft)", f"{average_price:,.0f} Ft")
    col3.metric("Average Size (sqm)", f"{average_size:.2f}")

    st.subheader("Visualizations")

    st.write("### Price Distribution")
    price_hist = (
        alt.Chart(filtered_data)
        .mark_bar()
        .encode(
            alt.X("price", bin=alt.Bin(maxbins=30), title="Price (Ft)"),
            y="count()",
        )
        .properties(width=600, height=400)
    )
    st.altair_chart(price_hist, use_container_width=True)

    st.write("### Price vs. Place Size")
    price_size_scatter = (
        alt.Chart(filtered_data)
        .mark_circle(size=60, opacity=0.7)
        .encode(
            x=alt.X("place_size", title="Place Size (sqm)"),
            y=alt.Y("price", title="Price (Ft)"),
            tooltip=["place_size", "price", "type", "property_location"],
        )
        .properties(width=600, height=400)
    )
    st.altair_chart(price_size_scatter, use_container_width=True)

    st.write("### Average Price by Property Type")
    avg_price_by_type = filtered_data.groupby("type")["price"].mean().reset_index()
    avg_price_type_chart = (
        alt.Chart(avg_price_by_type)
        .mark_bar()
        .encode(
            x=alt.X("type", title="Property Type"),
            y=alt.Y("price", title="Average Price (Ft)"),
            color="type",
        )
        .properties(width=600, height=400)
    )
    st.altair_chart(avg_price_type_chart, use_container_width=True)

    st.subheader("Additional Analysis")

    st.write("### Average Place Size by Number of Rooms")
    avg_size_by_rooms = (
        filtered_data.groupby("rooms")["place_size"].mean().reset_index()
    )
    avg_size_rooms_chart = (
        alt.Chart(avg_size_by_rooms)
        .mark_line(point=True)
        .encode(
            x=alt.X("rooms", title="Number of Rooms"),
            y=alt.Y("place_size", title="Average Place Size (sqm)"),
        )
        .properties(width=600, height=400)
    )
    st.altair_chart(avg_size_rooms_chart, use_container_width=True)

    st.write("### Median Price by Number of Rooms")
    median_price_by_rooms = (
        filtered_data.groupby("rooms")["price"].median().reset_index()
    )
    median_price_rooms_chart = (
        alt.Chart(median_price_by_rooms)
        .mark_line(point=True)
        .encode(
            x=alt.X("rooms", title="Number of Rooms"),
            y=alt.Y("price", title="Median Price (Ft)"),
        )
        .properties(width=600, height=400)
    )
    st.altair_chart(median_price_rooms_chart, use_container_width=True)

    st.write("### Price per Square Meter Distribution")
    filtered_data = filtered_data[filtered_data["place_size"] > 0]
    filtered_data["price_per_sqm"] = (
        (filtered_data["price"] / filtered_data["place_size"]).round(0).astype(int)
    )
    price_per_sqm_hist = (
        alt.Chart(filtered_data)
        .mark_bar()
        .encode(
            alt.X(
                "price_per_sqm",
                bin=alt.Bin(maxbins=30),
                title="Price per Square Meter (Ft)",
            ),
            y="count()",
        )
        .properties(width=600, height=400)
    )
    st.altair_chart(price_per_sqm_hist, use_container_width=True)

    st.write("### Correlation Heatmap")
    numeric_columns = filtered_data.select_dtypes(include=["float64", "int64"]).columns
    corr = filtered_data[numeric_columns].corr().reset_index().melt("index")
    corr_chart = (
        alt.Chart(corr)
        .mark_rect()
        .encode(
            x=alt.X("index", title=""),
            y=alt.Y("variable", title=""),
            color=alt.Color(
                "value",
                title="Correlation",
                scale=alt.Scale(scheme="bluepurple", domain=[-1, 1]),
            ),
            tooltip=["index", "variable", "value"],
        )
        .properties(width=600, height=600)
    )
    st.altair_chart(corr_chart, use_container_width=True)

    logging.info("Data visualization completed.")

    logging.info("Real estate data processing application finished successfully.")


if __name__ == "__main__":
    main()

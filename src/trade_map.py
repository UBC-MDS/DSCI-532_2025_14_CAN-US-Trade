import geopandas as gpd
import pandas as pd
import altair as alt
import numpy as np
import os
import pyproj

# Ensure PROJ_LIB is set correctly for geospatial operations
if "PROJ_LIB" not in os.environ:
    os.environ["PROJ_LIB"] = pyproj.datadir.get_data_dir()

# File paths
CLEAN_DATA_PATH = "data/clean/clean.csv"
GEOJSON_URL = "https://naciscdn.org/naturalearth/50m/cultural/ne_50m_admin_1_states_provinces.zip"

def create_trade_map(year=2014, trade_type="Export", category="All sections", geo_filter="Canada"):
    """
    Creates an Altair choropleth map of Canada showing trade data with hover highlighting.

    Args:
        year (int): The year to filter data.
        trade_type (str): The trade type to filter data (e.g., 'Export', 'Import').
        category (str): The goods/services category to filter by (default: "All sections").
        geo_filter (str): "Canada" for full view or a province/territory name.

    Returns:
        alt.Chart: Altair choropleth map visualization.
    """
    df = pd.read_csv(CLEAN_DATA_PATH, dtype={"YEAR": int}, parse_dates=["YEAR"], date_format="%Y")

    # Normalize province names for consistency
    df["GEO"] = df["GEO"].replace({"Quebec": "Québec"})  
    geo_filter = "Québec" if geo_filter == "Quebec" else geo_filter  

    # Standardize category filtering
    df["CATEGORY"] = df["CATEGORY"].str.strip().str.lower()
    category = category.strip().lower()

    # Filter data based on selections
    df = df[(df["YEAR"].dt.year == year) & (df["TRADE"] == trade_type)]
    if category != "all sections":
        df = df[df["CATEGORY"] == category]

    # Load Canadian provinces' geospatial data
    provinces = gpd.read_file(GEOJSON_URL)
    canadian_provinces = provinces[provinces["iso_a2"] == "CA"]

    # Filter map for a specific province if selected
    if geo_filter != "Canada":
        df = df[df["GEO"] == geo_filter]
        canadian_provinces = canadian_provinces[canadian_provinces["name"] == geo_filter]

    # Merge trade data with geospatial data
    merged = canadian_provinces.merge(df, left_on="name", right_on="GEO", how="left")

    # Handle missing values and log transform trade values
    merged["VALUE"] = merged["VALUE"].fillna(1e-3)
    merged = merged[merged["VALUE"] > 0]
    merged["LOG_VALUE"] = np.log10(merged["VALUE"])

    # Define color scale range based on percentiles
    q1, q99 = merged["LOG_VALUE"].quantile([0.01, 0.99])
    scale_domain = [q1, q99]

    # Define hover interaction
    hover = alt.selection_point(fields=["name"], on="mouseover", empty="none")

    # Construct the Altair choropleth map
    trade_map = (
        alt.Chart(merged)
        .mark_geoshape(stroke="white")
        .project("transverseMercator", rotate=[90, 0, 0])
        .encode(
            color=alt.Color(
                "LOG_VALUE:Q", 
                scale=alt.Scale(type="log", scheme="viridis", domain=scale_domain, clamp=True), 
                legend=alt.Legend(
                    title="Trade Value (CAD, Log10 Scale)", 
                    orient="bottom",
                    format=".2f"
                )
            ),
            stroke=alt.condition(hover, alt.value("black"), alt.value("white")),
            strokeWidth=alt.condition(hover, alt.value(3), alt.value(1)),
            tooltip=[
                "GEO:N", 
                alt.Tooltip("VALUE:Q", format=",.0f"),
                "CATEGORY:N"
            ]
        )
        .add_params(hover)
        .properties(
            width=900,  # Increased width for better visibility
            height=450,  # Increased height for better proportion
            title=alt.TitleParams(
                f"Trade Flow: {trade_type} in {year} ({category})",
                fontSize=20,
                fontWeight="bold"
            )
        )
    )
    return trade_map

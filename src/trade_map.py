# file: trade_map.py
# author: Elshaday Yoseph
# date: 2025-03-08

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

def create_trade_map(year, trade_type, category, geo_filter):
    """
    Generates an Altair choropleth map of Canada showing trade data with hover highlighting.

    Args:
        year (int): The year to filter data.
        trade_type (str): The trade type to filter data (e.g., 'Export', 'Import', 'Net trade').
        category (str): The goods/services category to filter by (default: "All sections").
        geo_filter (str): "Canada" for full view or a province/territory name.

    Returns:
        alt.Chart: Altair choropleth map visualization.
    """
      
    df = pd.read_csv(CLEAN_DATA_PATH)

    # Normalize province names for consistency
    df["GEO"] = df["GEO"].replace({"Quebec": "Québec"})  
    geo_filter = "Québec" if geo_filter == "Quebec" else geo_filter  

    # Standardize category filtering
    df["CATEGORY"] = df["CATEGORY"].str.strip().str.lower()
    category = category.strip().lower()

    # Filter data based on selections
    df = df[(df["YEAR"] == year) & (df["TRADE"] == trade_type)]
    df = df[df["CATEGORY"] == category]

    # Load Canadian provinces' geospatial data
    provinces = gpd.read_file(GEOJSON_URL)
    canadian_provinces = provinces[provinces["iso_a2"] == "CA"]

    # Merge trade data with geospatial data (keep all provinces)
    merged = canadian_provinces.merge(df, left_on="name", right_on="GEO", how="left")

    # Ensure trade values exist (fill NaN with 0)
    merged["VALUE"] = merged["VALUE"].fillna(0)

    # Fix Import Values: Keep them as positive numbers
    if trade_type == "Import":
        merged["VALUE"] = merged["VALUE"].abs()  # Convert negative imports to positive

    # Ensure log transformation doesn't remove zeros
    merged["LOG_VALUE"] = np.sign(merged["VALUE"]) * np.log10(np.abs(merged["VALUE"]) + 1)



    # Apply Province Filtering *AFTER* merging
    if geo_filter != "Canada":
        merged = merged[merged["name"] == geo_filter]

    # Define color scales based on trade type
    if trade_type == "Net trade":
        max_val = max(abs(merged["LOG_VALUE"].min()), abs(merged["LOG_VALUE"].max()))  # Symmetric range
        color_scale = alt.Scale(
            domain=[-max_val, 0, max_val],  # Ensures balance between red & green
            range=["red", "white", "green"]  # Red for deficit, white for neutral, green for surplus
    )


    elif trade_type == "Import":
        color_scale = alt.Scale(
            domain=[merged["LOG_VALUE"].min(), merged["LOG_VALUE"].max()],
            scheme="blues"  # Use a blue scale for imports
        )
    elif trade_type == "Export":
        color_scale = alt.Scale(
            domain=[merged["LOG_VALUE"].min(), merged["LOG_VALUE"].max()],
            scheme="greens"  # Use a green scale for exports
        )



    # Define hover interaction
    hover = alt.selection_point(fields=["name"], on="mouseover", empty="none")

    # Construct the Altair choropleth map
    trade_map = (
    alt.Chart(merged)
    .mark_geoshape(stroke="black")  # Keep borders for all provinces
    .project("transverseMercator", rotate=[90, 0, 0])
    .encode(
        color=alt.Color(
            "LOG_VALUE:Q", 
            scale=color_scale, 
            legend=alt.Legend(title="Trade Value (CAD, Log10 Scale)")
        ),
        stroke=alt.value("black"),
        strokeWidth=alt.value(1),
        tooltip=[
            "GEO:N", 
            alt.Tooltip("VALUE:Q", format=",.0f", title="Trade Value (CAD)"),
            "CATEGORY:N"
        ]
    )
    .add_params(hover)
    .properties(
        width=500,
        height=320,
        title=alt.TitleParams(
            f"Trade Flow: {trade_type} in {year} ({category})",
            fontSize=20,
            fontWeight="bold"
        )
    )
)


    return trade_map

# file: data.py
# author: Danish Karlin Isa
# date: 2025-03-08

import pandas as pd

# Load and process cleaned trade data
CLEAN_DATA_PATH = "data/clean/clean.csv"
df = pd.read_csv(CLEAN_DATA_PATH)

# Extract unique values for dropdown options
unique_years = sorted(df["YEAR"].unique(), reverse=True)
unique_provinces = ["Canada"] + sorted([geo for geo in df["GEO"].unique() if geo != "Canada"])
unique_categories = sorted(df["CATEGORY"].dropna().unique())
unique_trade_types = sorted(df["TRADE"].unique())  

# Define color scheme
HEADER_BG_COLOR = "#343A40"  # Dark grey for header
SIDEBAR_BG_COLOR = "#FFFFF"
TEXT_COLOR = "black"

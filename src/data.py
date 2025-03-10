# file: data.py
# author: Danish Karlin Isa
# date: 2025-03-08

import pandas as pd

# Download data
try:
    url = "https://www150.statcan.gc.ca/t1/tbl1/en/dtl!downloadDbLoadingData.action?pid=1210017301&latestN=0&startDate=20140101&endDate=20240101&csvLocale=en&selectedMembers=%5B%5B%5D%2C%5B243%5D%2C%5B%5D%2C%5B%5D%5D&checkedLevels=0D1%2C0D2%2C2D1%2C2D2%2C3D1"

    raw_data = pd.read_csv(url)

    expected_colnames = [
        'REF_DATE','GEO', 'DGUID', 'Trading partner',
        'North American Product Classification System (NAPCS)',
        'Trade', 'UOM', 'UOM_ID', 'SCALAR_FACTOR', 'SCALAR_ID',
        'VECTOR', 'COORDINATE', 'VALUE', 'STATUS', 'SYMBOL',
        'TERMINATED', 'DECIMALS'
    ]

    if raw_data.columns.to_list() != expected_colnames:
        raise RuntimeError("Names/order of columns in newly downloaded .csv file does not meet expectations.")

    raw_data.to_csv("data/raw/raw.csv")

    tidy_data = raw_data.copy()
    new_col_names = {
        "REF_DATE": "YEAR",
        "GEO": "GEO",
        "North American Product Classification System (NAPCS)": "CATEGORY",
        "Trade": "TRADE",
        "VALUE": "VALUE"
    }

    tidy_data = tidy_data.rename(new_col_names, axis=1)
    tidy_data = tidy_data[["YEAR", "GEO", "CATEGORY", "TRADE", "VALUE"]]
    tidy_data["CATEGORY"] = [each[:-6] if each != 'All sections' else each for each in tidy_data["CATEGORY"]]
    tidy_data["VALUE"] *= 1e3

    wide_data = tidy_data.pivot_table(
        index=['YEAR', 'GEO', 'CATEGORY'], columns='TRADE', values='VALUE'
        ).reset_index()
    wide_data['Import'] = -wide_data['Import']
    wide_data['Net trade'] = wide_data['Export'] + wide_data['Import']

    df = wide_data.melt(
        id_vars=['YEAR', 'GEO', 'CATEGORY'], value_vars=['Export', 'Import', 'Net trade'],
        var_name='TRADE', value_name='VALUE'
    )

    df.to_csv("data/clean/clean.csv", index=False)

except:
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

# file: clean_data.py
# author: Danish Karlin Isa
# date: 2025-02-24

import pandas as pd

raw_path = "data/raw/raw.csv"
destination = "data/clean"

raw_data = pd.read_csv(raw_path)

if not isinstance(raw_data, pd.DataFrame):
    raise TypeError("Input must be a Pandas DataFrame.")

if raw_data.empty:
    raise ValueError("`data/raw/raw.csv` is empty.")

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
tidy_data["GEO"] = tidy_data["GEO"].astype("category")
tidy_data["CATEGORY"] = [each[:-6] if each != 'All sections' else each for each in tidy_data["CATEGORY"]]
tidy_data["CATEGORY"] = tidy_data["CATEGORY"].astype("category")
tidy_data["TRADE"] = tidy_data["TRADE"].astype("category")
tidy_data["VALUE"] *= 1e3

tidy_data.to_csv(destination + "/clean.csv", index=False)

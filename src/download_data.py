# file: download_data.py
# author: Danish Karlin Isa
# date: 2025-02-24

import pandas as pd

url = "https://www150.statcan.gc.ca/t1/tbl1/en/dtl!downloadDbLoadingData.action?pid=1210017301&latestN=0&startDate=20140101&endDate=20240101&csvLocale=en&selectedMembers=%5B%5B%5D%2C%5B243%5D%2C%5B%5D%2C%5B%5D%5D&checkedLevels=0D1%2C0D2%2C2D1%2C2D2%2C3D1"

destination = "data/raw"

data = pd.read_csv(url)

expected_colnames = [
    'REF_DATE','GEO', 'DGUID', 'Trading partner',
    'North American Product Classification System (NAPCS)',
    'Trade', 'UOM', 'UOM_ID', 'SCALAR_FACTOR', 'SCALAR_ID',
    'VECTOR', 'COORDINATE', 'VALUE', 'STATUS', 'SYMBOL',
    'TERMINATED', 'DECIMALS'
]

if data.columns.to_list() != expected_colnames:
    raise RuntimeError("Names/order of columns in newly downloaded .csv file does not meet expectations.")

data.to_csv(destination + "/raw.csv")

import pandas as pd
from dash import html
import dash_bootstrap_components as dbc

# File path for cleaned trade data
CLEAN_DATA_PATH = "data/clean/clean.csv"

def generate_summary(year=2014, geo_filter="Canada", category="All sections"):
    """
    Generates a trade summary for a selected year, province/territory, and category.

    Args:
        year (int): The selected year.
        geo_filter (str): The selected province/territory or "Canada" for all.
        category (str): The selected goods/services category.

    Returns:
        dict: A dictionary containing net trade balance, exports, and imports.
    """
    df = pd.read_csv(CLEAN_DATA_PATH, dtype={"YEAR": int}, parse_dates=["YEAR"], date_format="%Y")

    # Filter data based on user selections
    df = df[df["YEAR"].dt.year == year]
    if geo_filter != "Canada":
        df = df[df["GEO"] == geo_filter]
    if category != "All sections":
        df = df[df["CATEGORY"] == category]

    # Calculate trade statistics
    exports = df[df["TRADE"] == "Export"]["VALUE"].sum()
    imports = df[df["TRADE"] == "Import"]["VALUE"].sum()
    net_trade = exports - imports

    return {"exports": exports, "imports": imports, "net_trade": net_trade}

def format_large_number(value):
    """
    Formats large numbers to display in millions (M) with commas.

    Args:
        value (float): The number to format.

    Returns:
        str: Formatted number string in millions (M).
    """
    return f"CA$ {value/1e6:,.0f}M"

def create_summary_component(year=2014, geo_filter="Canada", category="All sections"):
    """
    Creates a summary component displaying trade statistics in a 2-row layout.

    Args:
        year (int): The selected year.
        geo_filter (str): The selected province/territory or "Canada" for all.
        category (str): The selected goods/services category.

    Returns:
        html.Div: Dash component containing trade summary.
    """
    summary_data = generate_summary(year, geo_filter, category)

    # Format numbers for display
    net_trade = f"{format_large_number(summary_data['net_trade'])}"
    exports = f"{format_large_number(summary_data['exports'])}"
    imports = f"{format_large_number(summary_data['imports'])}"

    return dbc.Container([
        html.H5("Static Summary", className="text-center", style={"color": "red", "font-weight": "bold"}),
        html.H2(geo_filter, className="text-center", style={"font-weight": "bold"}),
        html.H3(year, className="text-center text-primary", style={"font-weight": "bold"}),

        # Category Section
        dbc.Card([
            dbc.CardBody([
                html.H5(category, className="text-center", style={"font-size": "18px"})
            ])
        ], className="mb-3", style={"border": "2px solid black"}),

        # **Net Trade Balance Card**
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Net Trade Balance", className="text-center", style={"font-weight": "bold"}),
                        html.H2(net_trade, className="text-center", style={"color": "#007BFF", "font-weight": "bold"})
                    ])
                ], className="shadow-sm p-3 mb-3", style={"border-radius": "10px"})
            ], width=12)  # Full width row
        ]),

        # **Exports & Imports Cards**
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Total Exports", className="text-center", style={"font-weight": "bold"}),
                        html.H2(exports, className="text-center", style={"color": "#28A745", "font-weight": "bold"})
                    ])
                ], className="shadow-sm p-3 mb-3", style={"border-radius": "10px"})
            ], width=6),  # Half width

            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Total Imports", className="text-center", style={"font-weight": "bold"}),
                        html.H2(imports, className="text-center", style={"color": "#DC3545", "font-weight": "bold"})
                    ])
                ], className="shadow-sm p-3 mb-3", style={"border-radius": "10px"})
            ], width=6)  # Half width
        ])
    ], fluid=True, className="p-3")

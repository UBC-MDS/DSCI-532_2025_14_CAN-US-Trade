import os
import pandas as pd
from dash import html
import dash_bootstrap_components as dbc

if "RENDER" in os.environ:
    from src.data import *
else:
    from data import *


def generate_summary(year=2024, geo_filter="Canada", category="All sections"):
    """
    Generates a trade summary for a selected year, province/territory, and category.

    Args:
        year (int): The selected year.
        geo_filter (str): The selected province/territory or "Canada" for all.
        category (str): The selected goods/services category.

    Returns:
        dict: A dictionary containing net trade balance, exports, and imports.
    """
    data = df.copy()

    # Ensure correct filtering logic
    data = data[data["YEAR"] == year]
    if geo_filter == "Canada":
        data = data[data["GEO"] == "Canada"]
    else:
        data = data[data["GEO"] == geo_filter]

    if category == "All sections":
        data = data[data["CATEGORY"] == "All sections"]
    else:
        data = data[data["CATEGORY"] == category]

    # Fetch the correct trade values
    exports = data[data["TRADE"] == "Export"]["VALUE"].values[0]
    imports = data[data["TRADE"] == "Import"]["VALUE"].values[0]
    net_trade = data[data["TRADE"] == "Net trade"]["VALUE"].values[0]

    return {"exports": exports, "imports": imports, "net_trade": net_trade}

def format_large_number(value):
    """
    Formats large numbers to display in millions (M) if >= 1M, otherwise in thousands (K).

    Args:
        value (float): The number to format.

    Returns:
        str: Formatted number string.
    """
    if abs(value) >= 1e6:
        return f"CA$ {value / 1e6:,.0f}M"
    elif abs(value) >= 1e3:
        return f"CA$ {value / 1e3:,.0f}K"
    else:
        return f"CA$ {value:,.0f}"

def create_summary_component(year=2024, geo_filter="Canada", category="All sections"):
    """
    Creates a summary component displaying trade statistics including 
    total exports, imports, net trade balance, and selected category.

    Args:
        year (int): Selected year.
        geo_filter (str): Selected province/territory.
        category (str): Selected goods/services category.

    Returns:
        html.Div: Dash component containing trade summary.
    """
    summary_data = generate_summary(year, geo_filter, category)

    # Format numbers for display
    net_trade = f"{format_large_number(summary_data['net_trade'])}"
    exports = f"{format_large_number(summary_data['exports'])}"
    imports = f"{format_large_number(summary_data['imports'])}"

    return dbc.Container([
        html.H6("Static Summary", className="text-center", 
                style={"color": "red", "font-weight": "bold", "margin-bottom": "5px"}),
        
        html.H3(geo_filter, className="text-center", 
                style={"font-weight": "bold", "font-size": "20px", "margin-bottom": "5px"}),
        
        html.H4(year, className="text-center text-primary", 
                style={"font-weight": "bold", "font-size": "18px", "margin-bottom": "10px"}),

        # **Category and Net Trade Balance Cards (Single Row)**
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("Goods & Services", className="text-center", 
                                style={"font-weight": "bold", "color": TEXT_COLOR}),
                        html.P(category, className="text-center", 
                               style={"font-size": "20px", "color": TEXT_COLOR})
                    ])
                ], className="shadow-sm p-2 mb-2", style={
                    "border-radius": "12px", 
                    "height": "100%", 
                    "background-color": "white",  # White background
                    "border": "2px solid #DEE2E6"
                })
            ], width=6),

            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("Net Trade Balance", className="text-center", 
                                style={"font-weight": "bold", "color": TEXT_COLOR}),
                        html.P(net_trade, className="text-center", 
                               style={"color": "#007BFF", "font-weight": "bold", "font-size": "20px"})  # Blue for contrast
                    ])
                ], className="shadow-sm p-2 mb-2", style={
                    "border-radius": "12px", 
                    "height": "100%", 
                    "background-color": "white",  # White background
                    "border": "2px solid #DEE2E6"
                })
            ], width=6),
        ], className="g-2"),

        # **Exports & Imports Cards (Single Row)**
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("Total Exports", className="text-center", 
                                style={"font-weight": "bold", "color": TEXT_COLOR}),
                        html.P(exports, className="text-center", 
                               style={"color": "#28A745", "font-weight": "bold", "font-size": "20px"})  # Green for exports
                    ])
                ], className="shadow-sm p-2", style={
                    "border-radius": "12px", 
                    "height": "100%", 
                    "background-color": "white",  # White background
                    "border": "2px solid #DEE2E6"
                })
            ], width=6),

            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H6("Total Imports", className="text-center", 
                                style={"font-weight": "bold", "color": TEXT_COLOR}),
                        html.P(imports, className="text-center", 
                               style={"color": "#DC3545", "font-weight": "bold", "font-size": "20px"})  # Red for imports
                    ])
                ], className="shadow-sm p-2", style={
                    "border-radius": "12px", 
                    "height": "100%", 
                    "background-color": "white",  # White background
                    "border": "2px solid #DEE2E6"
                })
            ], width=6),
        ], className="g-2")
    ], fluid=True, className="p-3", style={
        "height": "100%", 
        "overflow": "hidden", 
        "background-color": "white",  # White background for the summary
        "border": "2px solid #DEE2E6", 
        "border-radius": "15px"
    })

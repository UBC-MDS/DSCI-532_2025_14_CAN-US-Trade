# file: components.py
# author: Danish Karlin Isa
# date: 2025-03-08

import os
import dash_vega_components as dvc
import dash_bootstrap_components as dbc
from dash import html, dcc, dash_table

if "RENDER" in os.environ:
    from src.data import *
else:
    from data import *

def truncate_text(text, max_length=25):
    """Truncate text to max_length and add '...' if it's longer"""
    return text if len(text) <= max_length else text[:max_length] + "..."

header = html.Div([
    html.H1("CAN-US Trade Relations Dashboard", className="text-center", 
            style={"color": "white", "padding": "15px"})
    ], style={"background-color": HEADER_BG_COLOR, "border-radius": "8px", "margin-bottom": "10px"}
)

sidebar = dbc.Col([
    html.Label("Province/Territory:", style={"color": TEXT_COLOR}),
    dcc.Dropdown(
        id="province-dropdown",
        options=[{"label": geo, "value": geo} for geo in unique_provinces],
        value=DEFAULT_PROVINCE,
        clearable=False, 
        className="mb-3"
    ),

    html.Label("Year:", style={"color": TEXT_COLOR}),
    dcc.Dropdown(
        id="year-dropdown",
        options=[{"label": str(y), "value": y} for y in unique_years],
        value=DEFAULT_YEAR,
        clearable=False, 
        className="mb-3"
    ),

    html.Label("Trade Type:", style={"color": TEXT_COLOR}),
    dcc.Dropdown(
        id="trade-type-dropdown",
        options=[{"label": trade, "value": trade} for trade in unique_trade_types],
        value=DEFAULT_TRADE,
        clearable=False, 
        className="mb-3"
    ),

    html.Label("Goods and Services:", style={"color": TEXT_COLOR}),
    dcc.Dropdown(
        id="goods-dropdown",
        options=[{"label": cat, "value": cat, "title": cat, "label": truncate_text(cat, 25)} for cat in unique_categories],
        value=DEFAULT_GOODS,
        clearable=False, 
        className="mb-3",
        style={
        "whiteSpace": "nowrap",
        "textOverflow": "ellipsis",
    }
    ),

    html.Div(
        dbc.Button('Reset selection', 
                   color="secondary",
                   id='reset-button', 
                   n_clicks=1)
    ),

    html.Hr(style={"border-top": "1px solid white"}),
    html.P(
        "This Dash application provides an interactive dashboard for visualizing trade relations between Canada and the US",
        className="text-center font-weight-bold", style={"color": TEXT_COLOR}),
    html.P(
        "Developed by: Danish Karlin Isa, Elshaday Yoseph, Wangkai Zhu", className="text-center font-weight-bold", style={"color": TEXT_COLOR}),
    html.P([
        "GitHub Repository: ", 
        html.A("GitHub Link", href="https://github.com/UBC-MDS/DSCI-532_2025_14_CAN-US-Trade", target="_blank", style={"color": "lightblue"})
        ], className="text-center"),
    html.P(
        "Last Updated: March 14, 2025", className="text-center", style={"color": TEXT_COLOR}),
    ], width=2, className="p-3", 
    style={"height": "100vh", "overflow-y": "auto", "background-color": SIDEBAR_BG_COLOR}
)

overview_map = dbc.Col([
    html.Iframe(id="trade-map", 
    style={"width": "100%", "height": "90%", "border": "2px solid #ccc", 
    "border-radius": "8px", "overflow": "hidden", "background-color": "white"})
    ], width=6
)

summary_container = dbc.Col([
    html.Div(id="summary-container", 
             style={"width": "100%", "height": "92%", "border-radius": "8px", 
                    "padding": "10px", "background-color": "white"})
    ], width=6
)

trade_composition = dbc.Col([
    html.H4("Trade Composition Figure", className="text-center"),
    html.Div(id="placeholder-1", style={"width": "100%", "height": "600px"}),
#    html.Div(id="placeholder-1", style={"width": "90%", "height": "auto", "min-height": "200px", "overflow": "hidden"})
    ], width=6
)

trade_trend = dbc.Col([
    html.H4("Trade Trend Graph", className="text-center"),
    html.Iframe(id="trend-chart", 
    style={"width": "100%", "height": "90%", "border": "none", 
           "border-radius": "8px", "overflow": "hidden", "background-color": "white"})
    ], width=6
)
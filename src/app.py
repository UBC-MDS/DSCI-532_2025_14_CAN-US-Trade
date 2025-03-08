"""
CAN-US Trade Relations Dashboard
Author: Elshaday Yoseph
Date: 2025-02-28
"""

import os
import pandas as pd
import dash
from dash import dcc, html, Output, Input
import dash_bootstrap_components as dbc

# Import necessary functions based on the environment (local vs. Render)
if "RENDER" in os.environ:
    from src.trade_map import create_trade_map
    from src.summary import create_summary_component
    from src.trend_graph import create_trend_graph
    from src.composition_figure import create_composition_figure
else:
    from trade_map import create_trade_map
    from summary import create_summary_component
    from trend_graph import create_trend_graph
    from composition_figure import create_composition_figure

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

# Initialize Dash app with Bootstrap for styling
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # Required for deployment

# Define App Layout
app.layout = dbc.Container(fluid=True, style={"height": "100vh", "overflow": "hidden", "background-color": "#f8f9fa"}, children=[
    dbc.Row([
        # Sidebar (Filters)
        dbc.Col([
            html.Label("Province/Territory:", style={"color": TEXT_COLOR}),
            dcc.Dropdown(
                id="province-dropdown",
                options=[{"label": geo, "value": geo} for geo in unique_provinces],
                value="Canada",
                className="mb-3"
            ),

            html.Label("Year:", style={"color": TEXT_COLOR}),
            dcc.Dropdown(
                id="year-dropdown",
                options=[{"label": str(y), "value": y} for y in unique_years],
                value=unique_years[0],
                className="mb-3"
            ),

            html.Label("Trade Type:", style={"color": TEXT_COLOR}),
            dcc.Dropdown(
                id="trade-type-dropdown",
                options=[{"label": trade, "value": trade} for trade in unique_trade_types],
                value="Export",
                className="mb-3"
            ),

            html.Label("Goods and Services:", style={"color": TEXT_COLOR}),
            dcc.Dropdown(
                id="goods-dropdown",
                options=[{"label": cat, "value": cat} for cat in unique_categories],
                value="All sections",
                className="mb-3"
            ),

            html.Hr(style={"border-top": "1px solid white"}),
            html.P("This Dash application provides an interactive dashboard for visualizing trade relations between Canada and the US",
                   className="text-center font-weight-bold", style={"color": TEXT_COLOR}),
            html.P("Developed by: Danish Karlin Isa, Elshaday Yoseph, Wangkai Zhu", className="text-center font-weight-bold", style={"color": TEXT_COLOR}),
            html.P([
                "GitHub Repository: ", 
                html.A("GitHub Link", href="https://github.com/UBC-MDS/DSCI-532_2025_14_CAN-US-Trade", target="_blank", style={"color": "lightblue"})
            ], className="text-center"),
            html.P("Last Updated: March 6, 2025", className="text-center", style={"color": TEXT_COLOR}),
        ], width=2, className="p-3", style={"height": "100vh", "overflow-y": "auto", "background-color": SIDEBAR_BG_COLOR}), 

        # Main Content Area
        dbc.Col([
            # HEADER
            html.Div([
                html.H1("CAN-US Trade Relations Dashboard", className="text-center", style={"color": "white", "padding": "15px"})
            ], style={"background-color": HEADER_BG_COLOR, "border-radius": "8px", "margin-bottom": "10px"}),

            # First Row - Map & Summary
            dbc.Row([
                dbc.Col([
                    html.Iframe(id="trade-map", 
                                style={"width": "100%", "height": "90%", "border": "2px solid #ccc", 
                                       "border-radius": "8px", "overflow": "hidden", "background-color": "white"})
                ], width=6),
                dbc.Col([
                    html.Div(id="summary-container", 
                             style={"width": "100%", "height": "92%", "border-radius": "8px", 
                                    "padding": "10px", "background-color": "white"})
                ], width=6)
            ], className="g-0", style={"height": "50vh"}),

            # Second Row - Composition Figure & Trend Graph (No Borders)
            dbc.Row([
                dbc.Col([
                    html.H4("Trade Composition Figure", className="text-center"),
                    # html.Iframe(id="placeholder-1", 
                    #             style={"width": "100%", "height": "90%", "border": "none", 
                    #                    "border-radius": "8px", "overflow": "hidden", "background-color": "white"})
                    html.Div(id="placeholder-1", style={"width": "100%", "height": "600px"})
                ], width=6),
                dbc.Col([
                    html.H4("Trade Trend Graph", className="text-center"),
                    html.Iframe(id="placeholder-2", 
                                style={"width": "100%", "height": "90%", "border": "none", 
                                       "border-radius": "8px", "overflow": "hidden", "background-color": "white"})
                ], width=6),
            ], className="g-0", style={"height": "50vh"})
        ], width=10, className="px-2")
    ])
])

# Callback to update the trade map
@app.callback(
    Output("trade-map", "srcDoc"),
    Input("year-dropdown", "value"),
    Input("province-dropdown", "value"),
    Input("trade-type-dropdown", "value"),
    Input("goods-dropdown", "value")
)
def update_trade_map(selected_year, selected_province, selected_trade, selected_category):
    try:
        trade_chart = create_trade_map(
            year=selected_year, trade_type=selected_trade,
            category=selected_category, geo_filter=selected_province
        )
        return trade_chart.to_html()
    except Exception:
        return "<h3>Error: Failed to load trade map. Check logs.</h3>"

# Callback to update the summary section
@app.callback(
    Output("summary-container", "children"),
    Input("year-dropdown", "value"),
    Input("province-dropdown", "value"),
    Input("goods-dropdown", "value")
)
def update_summary(selected_year, selected_province, selected_category):
    return create_summary_component(year=selected_year, geo_filter=selected_province, category=selected_category)

# Callback to update the trade composition figure
@app.callback(
    Output("placeholder-1", "children"),
    Input("year-dropdown", "value"),
    Input("province-dropdown", "value"),
    Input("trade-type-dropdown", "value")
)
def update_composition_figure(selected_year, selected_province, selected_trade):
    try:
        composition_chart = create_composition_figure(
            year_filter=selected_year, geo_filter=selected_province, trade_filter=selected_trade
        )
        return html.Div([
            dcc.Graph(figure=composition_chart) 
        ])
    except Exception:
        return "<h3>Error: Failed to load composition figure. Check logs.</h3>"

# Callback to update the trade trend graph
@app.callback(
    Output("placeholder-2", "srcDoc"),
    Input("province-dropdown", "value"),
    Input("goods-dropdown", "value")
)
def update_trend_graph(selected_province, selected_category):
    try:
        trend_chart = create_trend_graph(geo_filter=selected_province, category=selected_category)
        return trend_chart.to_html()
    except Exception:
        return "<h3>Error: Failed to load trend graph. Check logs.</h3>"

# Run the Dash application
if __name__ == '__main__':
    app.run_server(debug=True)
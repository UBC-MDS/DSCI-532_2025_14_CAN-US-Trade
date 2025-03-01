"""
CAN-US Trade Relations Dashboard
Author: Elshaday Yoseph
Date: 2025-02-28

This Dash application provides an interactive dashboard for visualizing
trade relations between Canada and the US. The dashboard includes:

1. A **Trade Map** to display trade flow across provinces/territories.
2. A **Trade Composition Figure** (Placeholder 1) showing the breakdown of trade categories.
3. A **Trade Trend Graph** (Placeholder 2) depicting trade trends over time.

Users can filter data by:
- Province/Territory
- Year
- Trade Type (Export, Import, Net Trade)
- Goods and Services Category
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
unique_years = sorted(df["YEAR"].unique(), reverse=True)  # Ensure descending order
unique_provinces = ["Canada"] + sorted([geo for geo in df["GEO"].unique() if geo != "Canada"])
unique_categories = sorted(df["CATEGORY"].dropna().unique())
unique_trade_types = sorted(df["TRADE"].unique())  

# Initialize Dash app with Bootstrap for styling
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # Required for deployment

# Define App Layout
app.layout = dbc.Container(fluid=True, children=[
    # Main Title
    html.H1("CAN-US Trade Relations Dashboard", className="text-center mt-3 mb-4"),

    dbc.Row([
        # Sidebar with Filters
        dbc.Col([
            html.H4("Filters", className="mb-3"),

            # Province Dropdown
            html.Label("Province/Territory:"),
            dcc.Dropdown(
                id="province-dropdown",
                options=[{"label": geo, "value": geo} for geo in unique_provinces],
                value="Canada",
                className="mb-3"
            ),

            # Year Dropdown
            html.Label("Year:"),
            dcc.Dropdown(
                id="year-dropdown",
                options=[{"label": str(y), "value": y} for y in unique_years],
                value=unique_years[0],  # Default to the latest year
                className="mb-3"
            ),

            # Trade Type Dropdown
            html.Label("Trade Type:"),
            dcc.Dropdown(
                id="trade-type-dropdown",
                options=[{"label": trade, "value": trade} for trade in unique_trade_types],
                value="Export",
                className="mb-3"
            ),

            # Goods and Services Dropdown
            html.Label("Goods and Services:"),
            dcc.Dropdown(
                id="goods-dropdown",
                options=[{"label": cat, "value": cat} for cat in unique_categories],
                value="All sections",
                className="mb-3"
            ),
        ], width=2, className="bg-light p-3", style={
            "position": "fixed", "height": "100vh", "overflow-y": "auto",
            "min-width": "250px", "max-width": "300px"
        }),

        # Main Content Area
        dbc.Col([
            html.Div([
                # Trade Map and Summary Row
                dbc.Row([
                    dbc.Col([
                        html.Iframe(id="trade-map", style={"width": "100%", "height": "600px", "border": "none"})
                    ], width=7),
                    
                    dbc.Col([
                        html.Div(id="summary-container", style={"width": "100%"})
                    ], width=5)
                ], className="mb-3"),

                # Trade Composition Figure (Placeholder 1) & Trade Trend Graph (Placeholder 2)
                dbc.Row([
                    dbc.Col([
                        html.H4("Trade Composition Figure", className="text-center"),
                        html.Iframe(id="placeholder-1", style={"width": "100%", "height": "600px", "border": "none"})
                    ], width=6, className="p-2"),
                    
                    dbc.Col([
                        html.H4("Trade Trend Graph", className="text-center"),
                        html.Iframe(id="placeholder-2", style={"width": "100%", "height": "600px", "border": "none"})
                    ], width=6, className="p-2"),
                ], className="mb-3")
            ], style={"height": "100vh", "margin-left": "300px"})
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
    """
    Updates the trade map visualization based on selected filters.
    """
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
    """
    Updates the trade summary component based on selected filters.
    """
    return create_summary_component(year=selected_year, geo_filter=selected_province, category=selected_category)

# Callback to update the trade composition figure in Placeholder 1
@app.callback(
    Output("placeholder-1", "srcDoc"),
    Input("year-dropdown", "value"),
    Input("province-dropdown", "value"),
    Input("trade-type-dropdown", "value")
)
def update_composition_figure(selected_year, selected_province, selected_trade):
    """
    Updates the trade composition figure (Placeholder 1) based on selected filters.
    """
    try:
        composition_chart = create_composition_figure(
            year_filter=selected_year, geo_filter=selected_province, trade_filter=selected_trade
        )
        return composition_chart.to_html()
    except Exception:
        return "<h3>Error: Failed to load composition figure. Check logs.</h3>"

# Callback to update the trade trend graph in Placeholder 2
@app.callback(
    Output("placeholder-2", "srcDoc"),
    Input("province-dropdown", "value"),
    Input("goods-dropdown", "value")
)
def update_trend_graph(selected_province, selected_category):
    """
    Updates the trade trend graph (Placeholder 2) based on selected filters.
    """
    try:
        trend_chart = create_trend_graph(geo_filter=selected_province, category=selected_category)
        return trend_chart.to_html()
    except Exception:
        return "<h3>Error: Failed to load trend graph. Check logs.</h3>"

# Run the Dash application
if __name__ == '__main__':
    app.run_server(debug=True)

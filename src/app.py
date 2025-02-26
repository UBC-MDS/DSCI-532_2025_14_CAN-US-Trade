import os
import pandas as pd
import dash
from dash import dcc, html, Output, Input
import dash_bootstrap_components as dbc
if "RENDER" in os.environ:
    from src.trade_map import create_trade_map
    from src.summary import create_summary_component
else:
    from trade_map import create_trade_map
    from summary import create_summary_component


# Load cleaned trade data
CLEAN_DATA_PATH = "data/clean/clean.csv"
df = pd.read_csv(CLEAN_DATA_PATH, dtype={"YEAR": int}, parse_dates=["YEAR"], date_format="%Y")

# Extract unique values for dropdown options
unique_years = sorted(df["YEAR"].dt.year.unique(), reverse=True)
unique_provinces = sorted(df["GEO"].unique())
unique_categories = ["All sections"] + sorted(df["CATEGORY"].dropna().unique())
unique_trade_types = sorted(df["TRADE"].unique())

# Initialize Dash app
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
            
            html.Label("Province/Territory:"),
            dcc.Dropdown(
                id="province-dropdown",
                options=[{"label": geo, "value": geo} for geo in unique_provinces],
                value="Canada",
                className="mb-3"
            ),
            
            html.Label("Year:"),
            dcc.Dropdown(
                id="year-dropdown",
                options=[{"label": str(y), "value": y} for y in unique_years],
                value=2024,
                className="mb-3"
            ),
            
            html.Label("Trade Type:"),
            dcc.Dropdown(
                id="trade-type-dropdown",
                options=[{"label": trade, "value": trade} for trade in unique_trade_types],
                value="Export",
                className="mb-3"
            ),
            
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
                # Trade Map and Summary
                dbc.Row([
                    dbc.Col([
                        html.Iframe(id="trade-map", style={"width": "100%", "height": "600px", "border": "none"})
                    ], width=7),  # Increased width for better visibility
                    
                    dbc.Col([
                        html.Div(id="summary-container", style={"width": "100%"})
                    ], width=5)  # Adjusted width to balance layout
                ], className="mb-3"),

                # Placeholder Sections for Future Extensions
                dbc.Row([
                    dbc.Col([
                        html.H4("Placeholder 1", className="text-center"),
                        html.Div(id="placeholder-1", className="border p-3", style={"height": "250px"})
                    ], width=6, className="p-2"),
                    
                    dbc.Col([
                        html.H4("Placeholder 2", className="text-center"),
                        html.Div(id="placeholder-2", className="border p-3", style={"height": "250px"})
                    ], width=6, className="p-2"),
                ], className="mb-3")
            ], style={"overflow-y": "auto", "height": "100vh", "margin-left": "300px"})
        ], width=10, className="px-2")
    ])
])

# Callback to Update the Trade Map
@app.callback(
    Output("trade-map", "srcDoc"),
    Input("year-dropdown", "value"),
    Input("province-dropdown", "value"),
    Input("trade-type-dropdown", "value"),
    Input("goods-dropdown", "value")
)
def update_trade_map(selected_year, selected_province, selected_trade, selected_category):
    """
    Updates the trade map based on selected filter values.
    
    Args:
        selected_year (int): Year selected in dropdown
        selected_province (str): Province/Territory selected in dropdown
        selected_trade (str): Trade type selected (Export/Import)
        selected_category (str): Goods and services category selected
    
    Returns:
        str: HTML representation of the Altair trade map
    """
    try:
        trade_chart = create_trade_map(
            year=selected_year, trade_type=selected_trade,
            category=selected_category, geo_filter=selected_province
        )
        return trade_chart.to_html()
    except Exception as e:
        return "<h3>Error: Failed to load trade map. Check logs.</h3>"

# Callback to Update the Summary Section
@app.callback(
    Output("summary-container", "children"),
    Input("year-dropdown", "value"),
    Input("province-dropdown", "value"),
    Input("goods-dropdown", "value")
)
def update_summary(selected_year, selected_province, selected_category):
    """
    Updates the summary component based on selected filter values.
    
    Args:
        selected_year (int): Year selected in dropdown
        selected_province (str): Province/Territory selected in dropdown
        selected_category (str): Goods and services category selected
    
    Returns:
        html.Div: Dash HTML component containing summary statistics
    """
    return create_summary_component(year=selected_year, geo_filter=selected_province, category=selected_category)

# Run the Dash App
if __name__ == '__main__':
    app.run_server(debug=True)

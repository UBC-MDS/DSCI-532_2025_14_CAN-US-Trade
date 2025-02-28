import os
import pandas as pd
import dash
from dash import dcc, html, Output, Input
import dash_bootstrap_components as dbc
import dash_vega_components as dvc


# Import necessary functions based on the environment (local vs. Render)
if "RENDER" in os.environ:
    from src.trade_map import create_trade_map
    from src.summary import create_summary_component
    from src.trend_graph import create_trend_graph
else:
    from trade_map import create_trade_map
    from summary import create_summary_component
    from trend_graph import create_trend_graph

# Load and process cleaned trade data
CLEAN_DATA_PATH = "data/clean/clean.csv"
df = pd.read_csv(CLEAN_DATA_PATH)

# Convert YEAR column to integers (extract year)
df["YEAR"] = pd.to_datetime(df["YEAR"]).dt.year  

# Extract unique values for dropdown options
unique_years = sorted(df["YEAR"].unique(), reverse=True)  # Ensure descending order
unique_provinces = ["Canada"] + sorted([geo for geo in df["GEO"].unique() if geo != "Canada"])
unique_categories = sorted(df["CATEGORY"].dropna().unique())
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
                value=unique_years[0],  # Default to the latest year
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
                dbc.Row([
                    dbc.Col([
                        html.Iframe(id="trade-map", style={"width": "100%", "height": "600px", "border": "none"})
                    ], width=7),
                    
                    dbc.Col([
                        html.Div(id="summary-container", style={"width": "100%"})
                    ], width=5)
                ], className="mb-3"),

                dbc.Row([
                    dbc.Col([
                        html.H4("Placeholder 1", className="text-center"),
                        html.Div(id="placeholder-1", className="border p-3", style={"height": "250px"})
                    ], width=6, className="p-2"),
                    
                    dbc.Col([
                        html.H4("Trade values by year", className="text-center"),
                        dvc.Vega(id="trend-graph", spec={})
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
    Updates the trade map based on selected filters.
    """
    try:
        trade_chart = create_trade_map(
            year=selected_year, trade_type=selected_trade,
            category=selected_category, geo_filter=selected_province
        )
        return trade_chart.to_html()
    except Exception as e:
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
    Updates the trade summary based on selected filters.
    """
    return create_summary_component(year=selected_year, geo_filter=selected_province, category=selected_category)

@app.callback(
    Output("trend-graph", "spec"),
    Input("province-dropdown", "value"),
    Input("goods-dropdown", "value")
)
def update_trend_graph(selected_province, selected_category):
    return (
        create_trend_graph(
            geo_filter=selected_province, category=selected_category
        ).to_dict(format='vega'))

if __name__ == '__main__':
    app.run_server(debug=True)

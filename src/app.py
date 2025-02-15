from dash import Dash, html, dcc
import dash_bootstrap_components as dbc

# Initialize the app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = dbc.Container([
    
    # Title
    html.H1("CAN-US Trade Relations Dashboard", className="text-center mt-3 mb-4"),

    # Sidebar + Main Content Layout
    dbc.Row([

        # Sidebar (Filters)
        dbc.Col([
            html.H4("Filters", className="mb-3"),
            
            html.Label("Province/Territory:"),
            dcc.Dropdown(id="province-dropdown", options=[], placeholder="Select Province", className="mb-2"),

            html.Label("Year:"),
            dcc.Dropdown(id="year-dropdown", options=[], placeholder="Select Year", className="mb-2"),

            html.Label("Trade Type:"),
            dcc.Dropdown(id="trade-type-dropdown", options=[], placeholder="Select Trade Type", className="mb-2"),

            html.Label("Goods and Services:"),
            dcc.Dropdown(id="goods-dropdown", options=[], placeholder="Select Goods/Services", className="mb-2"),
        ], width=3, className="bg-light p-3"),
        
        # Main Content (2x2 Grid for Visuals)
        dbc.Col([
            dbc.Row([
                dbc.Col([
                    html.H5("Trade Flow Map", className="text-center"),
                    dcc.Graph(id="trade-map")
                ], width=6),
                
                dbc.Col([
                    html.H5("Trade Summary", className="text-center"),
                    html.Div(id="summary-box", className="border p-3")
                ], width=6),
            ], className="mb-3"),

            dbc.Row([
                dbc.Col([
                    html.H5("Industry Breakdown (Treemap)", className="text-center"),
                    dcc.Graph(id="treemap")
                ], width=6),
                
                dbc.Col([
                    html.H5("Tariff Impact Chart", className="text-center"),
                    dcc.Graph(id="tariff-chart")
                ], width=6),
            ], className="mb-3"),
            
            # Time Slider
            dbc.Row([
                dbc.Col([
                    html.H5("Trade Trends Over Time", className="text-center"),
                    dcc.Graph(id="trade-trends"),
                    
                    html.Label("Select Time Range:", className="mt-3"),
                    dcc.Slider(
                        id="time-slider",
                        min=2015, max=2024, step=1, value=2019,
                        marks={i: str(i) for i in range(2015, 2025, 1)},
                        tooltip={"placement": "bottom", "always_visible": True}
                    )
                ], width=12, className="mt-4"),
            ])
        ], width=9)
    ])
])

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)

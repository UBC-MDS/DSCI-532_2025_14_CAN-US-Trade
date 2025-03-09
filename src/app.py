# file: app.py 
# for: CAN-US Trade Relations Dashboard
# author: Elshaday Yoseph
# date: 2025-02-28

import os
from dash import Dash
import dash_bootstrap_components as dbc

# Import necessary modules
if "RENDER" in os.environ:
    from src import callbacks
    from src.components import (
        header, overview_map, summary_container, trade_composition, 
        trade_trend, sidebar
    )
    from src.data import *
else:
    import callbacks
    from components import (
        header, overview_map, summary_container, trade_composition, 
        trade_trend, sidebar
    )
    from data import *

# Initialize Dash app with Bootstrap for styling
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server  # Required for deployment

# Define App Layout
app.layout = dbc.Container(fluid=True, style={"height": "100vh", "overflow": "hidden", "background-color": "#f8f9fa"}, children=[
    dbc.Row([
        # Sidebar (Filters)
        sidebar, 

        # Main Content Area
        dbc.Col([
            # HEADER
            header,

            # First Row - Map & Summary
            dbc.Row([
                overview_map,
                summary_container,
            ], className="g-0", style={"height": "50vh"}),

            # Second Row - Composition Figure & Trend Graph (No Borders)
            dbc.Row([
                trade_composition,
                trade_trend,
            ], className="g-0", style={"height": "50vh"})
        ], width=10, className="px-2")
    ])
])

# Run the Dash application
if __name__ == '__main__':
#   app.server.run(host='127.0.0.1', port='8888')
    app.run_server(debug=True)
    
# file: callbacks.py
# author: Danish Karlin Isa
# date: 2025-03-08

import os
from dash import Output, Input, callback, html, dcc
from flask_caching import Cache

# Import necessary modules
if "RENDER" in os.environ:
    from src.trade_map import create_trade_map
    from src.summary import create_summary_component
    from src.trend_graph import create_trend_graph
    from src.composition_figure import create_composition_figure
    from src.data import *
    from src.cache import cache
else:
    from trade_map import create_trade_map
    from summary import create_summary_component
    from trend_graph import create_trend_graph
    from composition_figure import create_composition_figure
    from data import *
    from cache import cache

# Callback to update the trade map
@callback(
    Output("trade-map", "srcDoc"),
    Input("year-dropdown", "value"),
    Input("province-dropdown", "value"),
    Input("trade-type-dropdown", "value"),
    Input("goods-dropdown", "value")
)
@cache.memoize()
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
@callback(
    Output("summary-container", "children"),
    Input("year-dropdown", "value"),
    Input("province-dropdown", "value"),
    Input("goods-dropdown", "value")
)
@cache.memoize()

def update_summary(selected_year, selected_province, selected_category):
    return create_summary_component(year=selected_year, geo_filter=selected_province, category=selected_category)

# Callback to update the trade composition figure
@callback(
    Output("placeholder-1", "children"),
    Input("year-dropdown", "value"),
    Input("province-dropdown", "value"),
    Input("trade-type-dropdown", "value")
)
@cache.memoize()
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
@callback(
    Output("trend-chart", "srcDoc"),
    Input("province-dropdown", "value"),
    Input("goods-dropdown", "value")
)
@cache.memoize()
def update_trend_graph(selected_province, selected_category):
    try:
        trend_chart = create_trend_graph(geo_filter=selected_province, category=selected_category)
        return trend_chart.to_html()
    except Exception:
        return "<h3>Error: Failed to load trend graph. Check logs.</h3>"

# Callback to reset to defaults
@callback(
    Output("province-dropdown", "value"),
    Output("year-dropdown", "value"),
    Output("trade-type-dropdown", "value"),
    Output("goods-dropdown", "value"),
    Output("reset-button", "n_clicks"),
    Input("reset-button", "n_clicks")
)
@cache.memoize()
def reset_dropdown_selection(clicks):
    if clicks > 0:
        return (
            DEFAULT_PROVINCE, 
            DEFAULT_YEAR, 
            DEFAULT_TRADE, 
            DEFAULT_GOODS,
            DEFAULT_N_CLICKS
        )

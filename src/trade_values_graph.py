# file: trade_values_graph.py
# author: Danish Karlin Isa
# date: 2025-02-26

import pandas as pd
import altair as alt

alt.data_transformers.enable('vegafusion')

def create_trade_values_graph(FILTER_GEO='Canada', FILTER_CATEGORY = 'All sections'):
    DATA_FROM = "data/clean/clean.csv"
    data = pd.read_csv(DATA_FROM)

    x_axis = alt.X('YEAR:O', title="Year", axis=alt.Axis(labelAngle=-45))
    y_axis = alt.Y('VALUE', title="Value (CA$)",
                axis=alt.Axis(labelExpr='format(datum.value / 1e6, "(,") + " M"'))
    tooltip = [
        alt.Tooltip('YEAR', title='Year'), 
        alt.Tooltip('GEO', title='Province/Territory'), 
        alt.Tooltip('CATEGORY', title='Type of goods and services'),
        alt.Tooltip('TRADE', title='Trade type'),
        alt.Tooltip('VALUE', title='Value', format='($,~')
    ]
    color = alt.Color('TRADE', title=None, 
                    legend=alt.Legend(orient='bottom'))

    bar_graph = alt.Chart(data).mark_bar(cursor="pointer").encode(
        x=x_axis,
        y=y_axis,
        color=color,
        tooltip=tooltip
    ).transform_filter(
        (alt.datum.GEO == FILTER_GEO) &
        (alt.datum.CATEGORY == FILTER_CATEGORY) &
        (alt.datum.TRADE != 'Net trade')
    )

    trendline = alt.Chart(data).encode(
        x=x_axis,
        y=y_axis,
        color=color,
        tooltip=tooltip
    ).transform_filter(
        (alt.datum.GEO == FILTER_GEO) &
        (alt.datum.CATEGORY == FILTER_CATEGORY) &
        (alt.datum.TRADE == 'Net trade')
    )

    final_chart = alt.layer(
        bar_graph,
        trendline.mark_line(color='red'),
        trendline.mark_circle(size=75, color='red', opacity=1),
        width='container'
    )

    return final_chart
# file: composition_figure.py
# author: Danish Karlin Isa
# date: 2025-02-28

import pandas as pd
import altair as alt

alt.data_transformers.enable('vegafusion')

def create_composition_figure(year_filter=2024, geo_filter='Canada', trade_filter='Net trade'):
    DATA_FROM = "data/clean/clean.csv"
    data = pd.read_csv(DATA_FROM)

    x_axis = alt.X('VALUE', title="Value (CA$)",
                axis=alt.Axis(labelExpr='format(datum.value / 1e6, "(,") + " M"'))
    y_axis = alt.Y('CATEGORY', title='Type of goods and services', sort='-x')
    tooltip = [
        alt.Tooltip('CATEGORY', title='Type of goods and services'),
        alt.Tooltip('TRADE', title='Trade type'),
        alt.Tooltip('VALUE', title='Value', format='($,~')
    ]
    color_condition = alt.condition(
        alt.datum.VALUE >= 0,
        alt.value('blue'),  # Color if condition is true
        alt.value('red')    # Color if condition is false
    )

    final_chart = alt.Chart(data).mark_bar(color='rebeccapurple').encode(
        x=x_axis,
        y=y_axis,
        color=color_condition,
        tooltip=tooltip
    ).transform_filter(
        (alt.datum.YEAR == year_filter) &
        (alt.datum.GEO == geo_filter) &
        (alt.datum.CATEGORY != 'All sections') &
        (alt.datum.TRADE == trade_filter)
    )

    return final_chart
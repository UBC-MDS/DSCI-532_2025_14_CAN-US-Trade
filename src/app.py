from dash import Dash, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import dash_vega_components as dvc
import altair as alt
import pandas as pd

alt.data_transformers.enable('vegafusion')

data_from = "data/clean/clean.csv"

data = pd.read_csv(data_from)
data.head()

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

def create_trend_graph(geo_filter='Canada', category = 'All sections'):
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
        (alt.datum.GEO == geo_filter) &
        (alt.datum.CATEGORY == category) &
        (alt.datum.TRADE != 'Net trade')
    )

    trendline = alt.Chart(data).encode(
        x=x_axis,
        y=y_axis,
        color=color,
        tooltip=tooltip
    ).transform_filter(
        (alt.datum.GEO == geo_filter) &
        (alt.datum.CATEGORY == category) &
        (alt.datum.TRADE == 'Net trade')
    )

    final_chart = alt.layer(
        bar_graph,
        trendline.mark_line(color='red'),
        trendline.mark_circle(size=75, color='red', opacity=1),
        width='container'
    )

    return final_chart.to_dict(format='vega')

app.layout = dbc.Container([
    dvc.Vega(id='trend_by_year', spec=create_trend_graph())
])

if __name__ == '__main__':
    app.run_server()

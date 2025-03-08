# # file: composition_figure.py
# # author: Danish Karlin Isa
# # date: 2025-02-28

import pandas as pd
import plotly.express as px

def create_composition_figure(year_filter=2024, geo_filter='Canada', trade_filter='Net trade'):
    DATA_FROM = "data/clean/clean.csv"
    data = pd.read_csv(DATA_FROM)

    # Filter the data
    filtered_data = data[
        (data['YEAR'] == year_filter) &
        (data['GEO'] == geo_filter) &
        (data['CATEGORY'] != 'All sections') &
        (data['TRADE'] == trade_filter)
    ]

    filtered_data["CATEGORY"] = filtered_data["CATEGORY"].apply(lambda x: x.replace(" ", "<br>"))
    filtered_data["VALUE"] = filtered_data["VALUE"].abs()  # Convert negative numbers to positive
    filtered_data["VALUE_LABEL"] = filtered_data["VALUE"].apply(lambda x: f"${x:,.0f}")

    # Create treemap
    fig = px.treemap(
        filtered_data, 
        path=[px.Constant("Total"), 'CATEGORY'],  # Group by category
        values='VALUE',  # Size of rectangles based on trade value
        color='VALUE',  # Color by value
        color_continuous_scale='sunset'  # Color gradient
    )

    fig.update_traces(
        textinfo="label+percent entry",  # Show both label and value
        hoverinfo="label+value",  # Show value only on hover
        textfont=dict(size=15),  # Increase font size
        texttemplate="%{label}<br>%{percentEntry:.1%}", # Show category + percentage
        customdata=filtered_data["VALUE_LABEL"],  # Use formatted values

        hovertemplate="<b>%{label}</b><br>" +  
                      "Value: %{customdata}<br>" +  
                      "Percentage: %{percentEntry:.1%}<extra></extra>"
    )

    fig.update_layout(
        showlegend=False,  # Hide the legend
        coloraxis_showscale=False, # Hide legends
        autosize=True,  # Let it adjust automatically
        width=700,  # Reduce width
        height=320,  # Reduce height to prevent cutoff
        margin=dict(t=0, l=0, r=0, b=0),  # Reduce extra margins
    )

    return fig
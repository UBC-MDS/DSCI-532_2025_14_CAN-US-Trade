---
title: "DSCI 532 Milestone 3"
subtitle: "Reflection (Group 14)"
author: 
    - "Danish Karlin Isa"
    - "Elshaday Yoseph"
    - "Wangkai Zhu"
date: "2025-03-01"
date-format: "long"
---

## Implementation of dashboard based on proposal

There is no update with regards to implementation of proposed components of
our dashboard as we have done so in Milestone 2:

- Sidebar for users to choose their filters
- Interactive map of Canada's provinces and territories
- Static summary of trade balance by year, province/territory, goods and services and trade type
- Interactive figure showing the composition of goods and services by year, province/territory and trade type
- Interactive bar graph with a trend line that shows the trade balance (net trade, imports and exports) over the past 11 years by province/territory

## App refinements

We have implemented several refinements:

- Changed the trade composition figure from a bar chart to a treemap for better visualisation
- Moved footer text to sidebar to make better use of space

We have also managed to modularise the code:

- `app.py` only contains the skeleton of our dashboard
- `components.py` contains all the individual cards for our components
- `callbacks.py` contains all callbacks
- `data.py` handles downloading, cleaning and loading of data

## Addressing feedback

We have addressed all of the instructor's feedback:

- Adding colour to our header
- Ensured appropriate font sizes for our figures
- Updated line width, size of marker and colour of trend line for better visibility
- Ensured consistent use of colour throughout the plot
- Added card for map
- Fixed horizontal scrolling issue with individual plots
- Resized plots such that there is no need for vertical scrolling

## Our current dashboard

What is good:

- Our dashboard at its current state is representative of the one in our proposal.
- It also looks a lot more presentable than previous Milestone as we have eliminated scrolling and made better use of the space.

Limitations of our dashboard:

- There is an issue with the dropdown boxes where the text of an option will be wrapped around and overlaps the option below.

Future improvements:

- 2-way callbacks such that clicking on the figures can also act as a filter.
- Support for narrow screens like smartphones.

## Challenging question

Not attempted.

---
title: "DSCI 532 Milestone 2"
subtitle: "Reflection (Group 14)"
author: 
    - "Danish Karlin Isa"
    - "Elshaday Yoseph"
    - "Wangkai Zhu"
date: "2025-03-01"
date-format: "long"
---

## Implementation of dashboard based on proposal

We have managed to implement all the proposed components of our dashboard:

-   Sidebar for users to choose their filters

-   Interactive map of Canada's provinces and territories

-   Static summary of trade balance by year, province/territory, goods and services and trade type

-   Interactive figure showing the composition of goods and services by year, province/territory and trade type

-   Interactive bar graph with a trend line that shows the trade balance (net trade, imports and exports) over the past 11 years by province/territory

## Implementation difficulties

-   The interactivity for most of the components are limited to showing more detailed information when hovering the cursor. We have yet to implement 2-way callbacks as we have not learnt it in class.

-   There is some text formatting issue with the sidebar, where the text for different filtering options overlap.

-   For the main dashboard, on some screens, the figures may not be displayed in full (the user has to horizontally scroll to see each figure) and the text wrapping may cause the static summary to look weird. This can be solved by zooming out, but we intend to fix this issue.

## Deviation from best practices

We were mostly focused on coding the figures and getting them on the dashboard for this Milestone. Some best practices that we may have overlooked include:

-   consistent fonts and reasonable and readable font sizes
-   the use of appropriate colours in our figures and text

We initially intended on using a tree map to show the composition of goods and services, but due to inexperience with `Plotly` and limited time, we changed it to an `Altair` bar graph.

## Our current dashboard

What is good:

-   We managed to get the skeleton of the dashboard up and running.
-   For most of the figures, we managed to create what we had in mind.

Limitations of our dashboard:

-   There are issues regarding the scaling of the figures with respect to the browser zoom settings.
-   It is not visually appealing as we did not coordinate the styling of individual components and the formatting of the text.

Future improvements:

-   2-way callbacks such that clicking on the figures can also act as a filter.
-   Support for narrow screens like smartphones.
-   Respond faster to changes in filter values.
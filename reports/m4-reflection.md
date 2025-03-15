---
title: "DSCI 532 Milestone 4"
subtitle: "Reflection (Group 14)"
author: 
    - "Danish Karlin Isa"
    - "Elshaday Yoseph"
    - "Wangkai Zhu"
date: "2025-03-17"
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

## Addressing feedback

We have managed to address feedback from the instructor as well as peers:

- Using a more muted tone of green and red for the trade values graph to improve readability/visibility
- Allocating discrete colour categories for trade composition figure
- Fixed text wrapping issue for dropdown filters (long text previously wrapped around and overlapped the options below it such that the options below were covered)
- Added reset button that resets all dropdown filters to default values
- Fixed vanishing province issues, where provinces vanish from the map if the trade value is below 0

## Performance improvements

We have managed to implement several performance improvements:

- Loaded data faster by using `.parquet` binary format instead of `.csv` and `.shp`. We have also included a fallback that downloads a fresh copy of the data files if the `.parquet` files are corrupted.
- Consolidated all data processing for individual figures into `data.py` and ensured that all components of the dashboard use the same DataFrame by including the following line in the header:

```{python}
from data import *
```

- Ensured all functions used in data-wrangling are not row-wise operations
- Implemented caching for all figures

## App refinement

text here

## Our current dashboard

What is good:

- test

Limitations of our dashboard:

- test

Future improvements:

- 2-way callbacks such that clicking on the figures can also act as a filter.
- Support for narrow screens like smartphones.

## Notes

We faced an issue while resolving a merge conflict involving a binary file that could not be solved in the web editor. We faced some difficulty trying to resolve it locally too and while troublesooting, one of our members managed to inadvertently bypassed all branch protection rules and managed forcibly merged one of the branches into main by accident. This resulted in our commit history looking rather messy and we were not able to tidy it up. Fortunately our dashboard was not broken but we do realise that we got lucky with this. After this incident we checked the branch protection rules to ensure that bypassing branch protection rules is not allowed.

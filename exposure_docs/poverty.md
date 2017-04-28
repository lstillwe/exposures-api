# Exposure to Poverty (poverty)

**Last Updated**: 04/28/2017

## Overview
- **Data Source**: US Census Bureau – Poverty ([https://www.census.gov/topics/income-poverty/poverty/data/data-tools.html](https://www.census.gov/topics/income-poverty/poverty/data/data-tools.html)); secondary source is the American Community Survey via data.world ([https://data.world/uscensusbureau/?utm_source=autopilot&utm_medium=email&utm_content=170405&utm_campaign=feature_update](https://data.world/uscensusbureau/?utm_source=autopilot&utm_medium=email&utm_content=170405&utm_campaign=feature_update))*- **Input**: EXPest, income, age, # people in family- **Output**: categorical poverty exposure score (at/below or above poverty level)Poverty lines are defined by year and are based on income, age (< or ≥ 65 years), and number of people in the family. Tables for poverty cutoffs can be found at: [http://www.census.gov/data/tables/time-series/demo/income-poverty/historical-poverty-thresholds.html](http://www.census.gov/data/tables/time-series/demo/income-poverty/historical-poverty-thresholds.html).Poverty exposure 'score':

```1 if ≤ poverty line0 if otherwise
```Caveats re missing data points for inputs:- Age: if unknown, assume < 65 years- Income: if unknown, use US Census Tract median household income- Family size: if unknown, use 4**Caveat**: If the time period [`Ts,Te`] crosses multiple years, then use the category for the most recent year**Caveat**: Note that the US Census Bureau data are only available for census years; if data from a specific time period are unavailable, then use the most recent data available ***Note**: The ACS data will not be used for Green Team’s initial models

## Implemented as

Code: 

- TODO (poverty.py)

Details:

- TODO
# Exposure to Socioeconomic Status (ses)

**Last Updated**: 05/02/2017

## Overview

- **Data Source**: US Census Bureau – Poverty ([https://www.census.gov/topics/income-poverty/poverty/data/data-tools.html](https://www.census.gov/topics/income-poverty/poverty/data/data-tools.html)); secondary source is the American Community Survey via data.world ([https://data.world/uscensusbureau/?utm_source=autopilot&utm_medium=email&utm_content=170405&utm_campaign=feature_update](https://data.world/uscensusbureau/?utm_source=autopilot&utm_medium=email&utm_content=170405&utm_campaign=feature_update))*
- **Input**: EXPest, % US Census Tract population below poverty line
- **Output**: categorical SES exposure score (low, lower-middle, upper-middle, high)

'SES' can be defined in a variety of ways (e.g., income, poverty, housing, education, etc.); for the time being, we propose using US Census Tract data on income and the following formulations from [14] and [15]

SES exposure 'scores' (based on the percentage of US Census Tract population living below the poverty line)[14]  

```
1 = High SES (0%–4.9%)
2 = Upper-middle SES (5.0%–9.9%)
3 = Lower-middle SES (10.0%–19.9%)
4 = Low SES (≥ 20.0%)
```

**Caveat**: If the time period [`Ts,Te`] crosses multiple years, then use the category for the most recent year

**Caveat**: Note that the US Census Bureau data are only available for census years; if data from a specific time period are unavailable, then use the most recent data available 

**Caveat**: Many different measures of SES are used in literature; for example [9]: US Census Tract–level concentrated disadvantage scores based on 1990 US Census data was a simple sum of the following: % in poverty + % unemployed + % female-headed households + (100 - % college graduate).

***Note**: The ACS data will not be used for Green Team’s initial models

## References
https://github.com/mjstealey/datatranslator/blob/develop/exposure_docs/references.md

## Implemented as

Code: 

- TODO (ses.py)

Details:

- TODO

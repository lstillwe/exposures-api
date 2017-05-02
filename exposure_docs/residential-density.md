# Exposure to Residential Density (res_den)

**Last Updated**: 04/28/2017

## Overview

- **Data Source**: Primary source is US Census Bureau - Geography ([https://www.census.gov/geo/reference/urban-rural.html](https://www.census.gov/geo/reference/urban-rural.html)); secondary source is the American Community Survey via data.world ([https://data.world/uscensusbureau/?utm_source=autopilot&utm_medium=email&utm_content=170405&utm_campaign=feature_update](https://data.world/uscensusbureau/?utm_source=autopilot&utm_medium=email&utm_content=170405&utm_campaign=feature_update))*
- **Input**: EXPest, US Census Tract population size
- **Output**: categorical residential density exposure score (UA, UC, rural)

Residential density is based on location of home residence and US Census designation for that location

Residential density exposure ‘scores’:

```
1 = Urbanized Areas (UAs) of 50,000 or more people
2 = Urban Clusters (UCs) of at least 2,500 and less than 50,000 people
3 = Rural (not UA or UC)
```

**Caveat**: If the time period [Ts,Te] crosses multiple years, then use the category for the most recent year

**Caveat**: Note that the US Census Bureau data are only available for census years; if data from a specific time period are unavailable, then use the most recent data available 

***Note**: The ACS data will not be used for Green Team’s initial models

## Implemented as

Code: 

- TODO (res_den.py)

Details:

- TODO

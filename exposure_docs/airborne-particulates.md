# Exposure to Airborne Particulates (pm25)

**Last Updated**: 04/28/2017

## Overview

- **Data Source**: US EPA via the Center for Community Modeling and Assessment System, UNC Institute for the Environment 
- **Input**: EXPest
- **Output**: categorical exposure score, ranging from 1 (low) to 5 (high)

***Note**: In addition to (or instead of) the spatial-temporal exposure model developed above and based on [1], UNC’s CMAS Center has developed more sophisticated models—CMAQ, R-LINE, C-LINE—which provide more accurate and granular exposure measures that take into account factors such as time of day, humidity, wind flow, etc. In the near-term, we will work with CMAQ 2010 (36-km resolution) and 2011 (12-km resolution) data on primary and secondary PM2.5 and secondary ozone exposures. (Note that ozone exposures are all secondary.) Eventually, the following exposure measures will be made available from the CMAS roadside exposure models, either as yearly averages or as hourly values (which require assumed conditions on season, time of day, wind direction, atmospheric stability, day of week, hour of day).  

***Note** that PM2.5 will be the primary (socio)environmental exposure measure for the Translator Demonstration Use Case because the PM2.5-asthma linkage is well documented and the other exposures will present the same challenges, so PM2.5 provides a good stress test of our model and approach.

Available measurements:

- NOx: nitrogen oxides; maximum: 200 ppb
- CO: carbon monoxide; maximum: 10,000 ppb
- SOx: sulfur dioxide; maximum: 100 ppb
- PM2.5: particulate matter with aerodynamic diameter <2.5 microns; maximum: 50 μg/m3
- Diesel-PM2.5: PM2.5 emissions from diesel vehicles only; maximum: 50 μg/m3
- EC2.5: portion of PM2.5 consisting of elemental carbon (graphitic carbon and high molecular weight, nonvolatile organic compounds); maximum: 50 μg/m3
- OC2.5: portion of PM2.5 consisting of organic carbon (particulate organic compounds containing more than 20 carbon atoms); maximum: 50 μg/m3
- Benzene: maximum: 30 μg/m3
- Formaldehyde: maximum: 9.8 μg/m3
- Acetaldehyde: (systematic name: ethanol); maximum: 9 μg/m3
- Acrolein: (systematic name: propenal); maximum: 0.02 μg/m3
- 1,3-butadiene: maximum: 2 μg/m3

## Exposure to Airborne Particulates - PM2.5

- **Data Source**: US EPA via the Center for Community Modeling and Assessment System, UNC Institute for the Environment
- **Input**: EXPest, geocoded estimates of PM2.5 concentrations
- **Output**: categorical PM2.5 exposure score, ranging from 1 (low) to 5 (high)

Daily PM2.5 exposure ‘score’ (DESpm):[2]

```
DESpm = 1 if 24h max PM2.5 < 4.0 μg/m3
DESpm = 2 if 24h max PM2.5 4.0-7.06 μg/m3
DESpm = 3 if 24h max PM2.5 7.07-8.97 μg/m3
DESpm = 4 24h max PM 2.5 8.98-11.36 μg/m3
DESpm = 5 if 24h max PM2.5 > 11.37 μg/m3
```

Overall 7- and 14-day PM2.5 exposure ‘scores’

```
DES7pm = (DESP1+DESP2…DESP7)/7
DES14pm = (DESP1+DESP2…DESP14)/14
```

**Caveat**: These cutoffs are based solely on [2], and they do not account for extreme weather days. The values are much lower than the US EPA AQI breakpoints, which provide benchmarks for all persons (children plus adults, healthy and non-healthy), are skewed toward extreme weather events, and are not as granular as we propose for pediatric patients with asthma, who are very sensitive to airborne pollutants. US EPA AQI breakpoints: 24-h average: 0-12, 12.1-35.4, 35.5-55.4, 55.5-150.4, 150.5-250.4, 250.5-350.4, 350.5-500.4 μg/m3 ([https://en.wikipedia.org/wiki/Air_quality_index](https://en.wikipedia.org/wiki/Air_quality_index))[3]. US EPA overall guidelines are maximum PM2.5:  12.0 μg/m3 over 1 year, 35 μg/m3 over 24 hours.

**Caveat**: This approach does not account for exposures prior to the Ts date, however, we are assuming that the impact of high exposures is relatively short (<1 or 2 weeks).

## Implemented as

Code: 

- [python-flask-server/exposures/pm25.py](../python-flask-server/exposures/pm25.py)

Details:

- TODO


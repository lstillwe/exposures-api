# Exposure to Crime/Violence (crime)

**Last Updated**: 04/28/2017

## Overview

- **Data Source**: US FBI Uniform Crime Reporting Program ([https://ucr.fbi.gov/](https://ucr.fbi.gov/))
- **Input**: EXPest, counts of ‘crime’ per 1,000 residents per reporting ‘district’
- **Output**: categorical crime exposure score (1–10)

Crime rates = counts per 1,000 residents of violent crime (murder, non-negligent manslaughter, forcible rape, robbery, aggravated assault) or property crime (burglary, larceny-theft, motor vehicle theft), measured at US Census–tract level and reported annually

Crime exposure 'score':[13]

```
1 (less crime) – 10 (more crime) relative to national distribution
```

**Caveat**: If the time period [`Ts,Te`] crosses multiple years, then use the most recent category

**Caveat**: The data are released annually, although there is a lag time, such that the most recent data available are from 2015; if data for a specific time period are unavailable, then use the most recent data available

**Caveat**: The cutoffs in [13] are based on proprietary models; we will need to identify appropriate cutoffs, perhaps by examining the overall distribution of crime rates (i.e., across the nation) and then statistically generating appropriate cutoffs

## References
https://github.com/mjstealey/datatranslator/blob/develop/exposure_docs/references.md

## Implemented as

Code: 

- TODO (crime.py)

Details:

- TODO

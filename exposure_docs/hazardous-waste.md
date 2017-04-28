# Exposure to Hazardous Waste (haz_waste)

**Last Updated**: 04/28/2017

## Overview
- **Data Source**: NC Department of Environmental Quality ([https://deq.nc.gov/about/divisions/waste-management/waste-management-rules-data/waste-management-gis-maps](https://deq.nc.gov/about/divisions/waste-management/waste-management-rules-data/waste-management-gis-maps)); US EPA Superfund Sites ([https://www.epa.gov/superfund/search-superfund-sites-where-you-live](https://www.epa.gov/superfund/search-superfund-sites-where-you-live))- **Input**: EXPest, distance from hazardous waste site- **Output**: categorical hazardous waste exposure score (low, medium, high)A variety of exposures are available from NC DEQ and the US Superfund Program; we will restrict our focus initially to four generally types of hazardous waste exposuresWaste exposure types:
- Active Disaster Debris Sites (ActiveDisaster)- Active Hazardous Waste Sites	- Small Quantity Generators (ActiveSQG)	- Large Quantity Generators (ActiveLQG)	- Treatment, Processing and Disposal Facilities (ActiveTreatment)- Inactive Hazardous Waste Sites (InactiveHazard)- Superfund Sites (Superfund)Hazardous waste exposure 'score':[7-12]

```1 = Low: home residence >50 miles from site2 = Medium: home residence 1-50 miles from site3 = High: home residence <1 mile from site
```**Caveat**: The data are available for both NC and the nation and are more or less static, although active sites may become inactive sites and superfund sites might be declared ‘clean’ at some point in the future**Note**: The categories are based on [7-12], with numerous studies showing an increased risk of cancer and a variety of other health outcomes, including those specific to pregnant women and children; as such, these exposures might represent a good point of synergy between Green Team and Blue Team

## Implemented as

Code: 
 
- TODO (haz_waste.py)

Details:

- TODO

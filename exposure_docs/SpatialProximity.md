## Issues regarding spatial queries and proximity - plus importance of precision

Accuracy is the tendency of your measurements to agree with the true values. Precision is the degree to which your measurements pin down an actual value. The question is about an interplay of accuracy and precision.

As a general principle, you don't need much more precision in recording your measurements than there is accuracy built into them. Using too much precision can mislead people into believing the accuracy is greater than it really is.

Generally, when you degrade precision--that is, use fewer decimal places--you can lose some accuracy. But how much? It's good to know that the meter was originally defined (by the French, around the time of their revolution when they were throwing out the old systems and zealously replacing them by new ones) so that ten million of them would take you from the equator to a pole. That's 90 degrees, so one degree of latitude covers about 10^7/90 = 111,111 meters. ("About," because the meter's length has changed a little bit in the meantime. But that doesn't matter.) Furthermore, a degree of longitude (east-west) is about the same or less in length than a degree of latitude, because the circles of latitude shrink down to the earth's axis as we move from the equator towards either pole. Therefore, it's always safe to figure that the sixth decimal place in one decimal degree has 111,111/10^6 = about 1/9 meter = about 4 inches of precision.

Accordingly, if your accuracy needs are, say, give or take 10 meters, than 1/9 meter is nothing: you lose essentially no accuracy by using six decimal places. If your accuracy need is sub-centimeter, then you need at least seven and probably eight decimal places, but more will do you little good.

Thirteen decimal places will pin down the location to 111,111/10^13 = about 1 angstrom, around half the thickness of a small atom.

Using these ideas we can construct a table of what each digit in a decimal degree signifies:

The sign tells us whether we are north or south, east or west on the globe.
A nonzero hundreds digit tells us we're using longitude, not latitude!
The tens digit gives a position to about 1,000 kilometers. It gives us useful information about what continent or ocean we are on.
The units digit (one decimal degree) gives a position up to 111 kilometers (60 nautical miles, about 69 miles). It can tell us roughly what large state or country we are in.

The first decimal place is worth up to 11.1 km: it can distinguish the position of one large city from a neighboring large city.

The second decimal place is worth up to 1.1 km: it can separate one village from the next.

The third decimal place is worth up to 110 m: it can identify a large agricultural field or institutional campus.

The fourth decimal place is worth up to 11 m: it can identify a parcel of land. It is comparable to the typical accuracy of an uncorrected GPS unit with no interference.

The fifth decimal place is worth up to 1.1 m: it distinguish trees from each other. Accuracy to this level with commercial GPS units can only be achieved with differential correction.

The sixth decimal place is worth up to 0.11 m: you can use this for laying out structures in detail, for designing landscapes, building roads. It should be more than good enough for tracking movements of glaciers and rivers. This can be achieved by taking painstaking measures with GPS, such as differentially corrected GPS.

The seventh decimal place is worth up to 11 mm: this is good for much surveying and is near the limit of what GPS-based techniques can achieve.

The eighth decimal place is worth up to 1.1 mm: this is good for charting motions of tectonic plates and movements of volcanoes. Permanent, corrected, constantly-running GPS base stations might be able to achieve this level of accuracy.

The ninth decimal place is worth up to 110 microns: we are getting into the range of microscopy. For almost any conceivable application with earth positions, this is overkill and will be more precise than the accuracy of any surveying device.

Ten or more decimal places indicates a computer or calculator was used and that no attention was paid to the fact that the extra decimals are useless. Be careful, because unless you are the one reading these numbers off the device, this can indicate low quality processing!
	
The Wikipedia page Decimal Degrees has a table on Degree Precision vs. Length. Also the accuracy of your coordinates depends on the instrument used to collect the coordinates - A-GPS used in cell phones, DGPS etc.


|decimal places| degrees     | distance |
|--------------|-------------|----------|
|0             |1            |111  km   |
|1             |0.1          |11.1 km   |
|2             |0.01         |1.11 km   |
|3             |0.001        |111  m    |
|4             |0.0001       |11.1 m    |
|5             |0.00001      |1.11 m    |
|6             |0.000001     |11.1 cm   |
|7             |0.0000001    |1.11 cm   |
|8             |0.00000001   |1.11 mm   |
|9             |0.000000001  |111  μm   |
|10            |0.0000000001 |11.1 μm   |

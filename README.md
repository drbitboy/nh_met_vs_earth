# nh_met_vs_earth
## Compare New Horizons clock to Earth rotation

The New Horizons (NH) spacecraft clock loses about one SI second per day, or about 1s per 3y.

The Earth as a clock, as measured by its rotation and tracked by UTC, has one leapsecond added every few years.

As such, the NH clock (MET; Mission Elapsed Time) runs roughly in synchrony with Earth UTC.

The script in this repository plots the difference between the NH MET with respect to a time near NH launch, and the corresponding non-leapsecond-corrected time, as implemented in the Python datetime module, with respect to that same time near launch.

![missing image](nh_met_vs_earth_rotation.png)

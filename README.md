# nh_met_vs_earth

## Summary

The following commands use BASH shell syntax to convert a pseudo-UTC to a New Horizons (H) Mission Event (Elapsed) Time (MET), to an accuracy of +/-1s:

    % let met=$(date --date="2015-07-14 11:50:00 +0000" +%s)-$(date --date="2006-01-19 18:08:02 +0000" +%s) ; echo $met
    299180518

    % let met=$(date --date="2019-01-01 05:33:22 +0000" +%s)-$(date --date="2006-01-19 18:08:02 +0000" +%s) ; echo $met
    408626720

The reverse conversion is performed like this:

    % date --date="2006-01-19 18:08:02 +0000 + 299180518 seconds" --utc +%Y-%m-%dT%H:%M:%S
    2015-07-14T11:50:00

    % date --date="2006-01-19 18:08:02 +0000 + 408626720 seconds" --utc +%Y-%m-%dT%H:%M:%S
    2019-01-01T05:33:22

See below for validation of results

## Compare New Horizons clock to Earth rotation

The New Horizons (NH) spacecraft clock loses about one SI millisecond per day, or just over 1s per 3y.

The Earth as a clock, as measured by its rotation and tracked by UTC, has one leapsecond added every few years.

As such, the NH clock (MET; Mission Elapsed Time) runs roughly in synchrony with Earth UTC sans leapseconds.

The script in this repository plots the difference between the NH MET with respect to a time near NH launch (19.January, 2006), and the corresponding non-leapsecond-corrected time, as implemented in the Python datetime module, with respect to that same time near launch.

The result shows that simple Unix-like time calculations time can be used to convert between NH MET and leapsecond-corrected UTC with an accuracy of around 1s.

![NH MET vs Earth rotation plot image](nh_met_vs_earth_rotation.png)

## Two Seconds of Fudge

The first and second triplets for SCLK01_COEFFICIENTS_98 in NH SCLK-Kernels (new-horizons_VVVV.tsc, where VVVV is version number e.g. 1767) have an inconsistent relationship.  Specifically, the TDBseconds/METseconds slope from the first line does not represent the ratio between the TDB and tick values.  Operationally this is not an issue since this anomaly only shows up for a duration of about 2.3s at about 15h after the SCLK zero time.

The second script, nh_met_2s_anomaly.py, demonstrates that the difference between the first and second TDB values should be about 2.3s less than it is.  In addition it generates the plot below, which shows the result, near that brief period, of starting with an ET, converting it to an SCLK ticks value, and then back to an ET, which should be equal to the starting ET.

![NH MET 2s Anomaly plot](nh_met_2s_anomaly.png)

## Validation of results

The following commands use the SPICE CHRONOS utility to make the same conversions

    % chronos -setup mk.tm -from utc -to sclk -time 2015-07-14T11:50:00
    3/0299180518:06211                                              (SCLK/SCLK)

    chronos -setup mk.tm -from utc -to sclk -time 2019-01-01T05:33:22
    3/0408626719:42579                                              (SCLK/SCLK)

The contents of the meta-kernel (MK) used in those CHRONOS commands, mk.tm:

    \begindata
    LEAPSECONDS_FILE = 'naif0012.tls'
    SCLK_FILE        = 'new-horizons_1767.tsc'
    SPACECRAFT_ID    = -98
    CENTER_ID        = -98
    \begintext


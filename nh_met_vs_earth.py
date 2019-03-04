import os
import datetime
import spiceypy as sp
import matplotlib.pyplot as plt

### Load LSK and SCLK kernels; initial list of kernel names
bn_kernels = list()
for k in """
naif0012.tls
new-horizons_1767.tsc
""".strip().split():
  sp.furnsh(k)
  ### Add kernel basename without extension
  bn_kernels.append(os.path.basename(k).split('.')[0])

### Convert list to string
s_kernels = '[{}]'.format(','.join(bn_kernels))

### Constants:  NH SCLK sub-ticks per NH tick second, seconds per year
tps, spy = 5e4, sp.jyear()

### Interpret datetime.datetime string as UTC and convert to MET seconds
date2met = lambda dayt: sp.sce2t(-98,sp.utc2et(dayt.strftime('%Y-%m-%dT%H:%M:%S'))) / tps

### Fudge factor; NH MET clock shifts 2s during the launch day
met_fudge = -2

### ET and date and MET, all 1d after SCLK zero time
et = sp.sct2e(-98,0.) - met_fudge
s_0 = sp.timout(et,'Sun MON DD HR:MN:SC YYYY',99)
date0 = datetime.datetime.strptime(s_0,'%c')
met0 = date2met(date0) + met_fudge

### Year, as a floating point value, at that time
offset_to_launch = 2000 + ((date0 - datetime.datetime(2000,1,1,12)).total_seconds() / spy)

### Time of leapsecond events, from LSK
leapsecs_met_y = [offset_to_launch + (sp.sce2t(-98,sp.utc2et(s.strip())) / (tps * spy))
for s in """
2009-JAN-1/00:00:00
2012-JUL-1/00:00:00
2015-JUL-1/00:00:00
2017-JAN-1/00:00:00
""".strip().split('\n')
]

### Current datetime.datetime object
now = datetime.datetime.now()

### Step size as datetime.timedelta object
d6 = datetime.timedelta(days=6)

### Initialize year (abscissa) and time difference (ordinate) lists
mets_y = list()
deltas = list()

### Step over dates until now, build lists
curdate = date0
while (now-curdate).total_seconds() > 0.:
  ### Step date
  curdate += d6
  ### Get delta from MET0 to MET corresponding to curdate
  dmet = date2met(curdate) - met0
  ### Convert dmet to year
  mets_y.append(offset_to_launch + (dmet / spy))
  ### Get difference betwwen dmet and (current date - date0) difference
  deltas.append(dmet - (curdate-date0).total_seconds())

### Plot red vertical lines at leapsecond events
label='Leapsecond events'
for leapsec in leapsecs_met_y:
  plt.axvline(leapsec,color='r',label=label)
  label=None

### Plot data as blue lines
plt.plot(mets_y,deltas,color='b')

### Annotations
plt.xlabel('MET, y (approx.)')
plt.ylabel('dMET - dUnixtime, s')
plt.title('New Horizons MET vs. Earth rotation seconds\n{} {}'.format(s_0[4:],s_kernels))

### Legend
plt.legend(loc='best')

### Show plot
plt.show()

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

### Constants:  NH SCLK sub-ticks per NH tick second
tps = 5e4

met0,et0,rate0,met1,et1,rate1 = sp.gdpool('SCLK01_COEFFICIENTS_98',0,6)

assert met0 == 0

correct_et0 = (et1 - ((met1-met0) * rate0 / tps))
error0 = et0 - correct_et0

tpictr='@YR-MON-DD-HR:MN:SC.##### ::TDB ::RND'

correct_tdb0 = sp.timout(correct_et0,tpictr,99)

print(dict(error0=error0,correct_tdb0=correct_tdb0))

abscissa = list()
ordinate = list()

et1s = [et1,et0+((met1-met0)*rate0/tps)]
start_et = min(et1s) - abs(error0)
stop_et = max(et1s) + abs(error0)

det = 0.
ddet = 0.1

et = start_et + det

while et <= stop_et:
  abscissa.append(det)
  ordinate.append(sp.sct2e(-98,sp.sce2t(-98,et))-et)
  det += ddet
  et = start_et + det

plt.plot(abscissa,ordinate)
plt.xlabel('s past {}'.format(sp.timout(start_et,tpictr,99)))
plt.ylabel('ET=>SCLKdp=>ET error, s')
plt.show()

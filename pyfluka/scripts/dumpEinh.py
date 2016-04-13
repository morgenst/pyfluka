__author__ = 'marcusmorgenstern'
__mail__ = ''

import pickle
import re

from pyfluka.utils import ureg

from pyfluka.utils import PhysicsQuantities as PQ

fIn = open("../data/StSV_Annex3.csv", "r")
einh_vals = {}

for line in fIn.readlines()[3:]:
    if not re.match("^[A-Z]", line):
        continue
    line = line.replace('\n', '')
    sl = line.split(',')
    einh_vals[PQ.Isotope(int(re.findall(r'\d+', sl[0])[0]),
                      sl[0].split('-')[0],
                      1 if sl[0].endswith("m") else 0)] = PQ.EInh(float(sl[1]), ureg.Sv / ureg.Bq)

fIn.close()
fOut = open("../data/inhalation.p", 'w')
pickle.dump(einh_vals, fOut)
fOut.close()

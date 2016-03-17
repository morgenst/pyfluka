__author__ = 'marcusmorgenstern'
__mail__ = ''

import pickle
import re
from utils import PhysicsQuantities as PQ
from utils import ureg

fIn = open("../data/StSV_Annex3.csv", "r")
eing_vals = {}

for line in fIn.readlines()[3:]:
    if not re.match("^[A-Z]", line):
        continue
    line = line.replace('\n', '')
    sl = line.split(',')
    eing_vals[PQ.Isotope(int(re.findall(r'\d+', sl[0])[0]),
                         sl[0].split('-')[0],
                         1 if sl[0].endswith("m") else 0)] = PQ.EIng(float(sl[2]), ureg.Sv / ureg.Bq)

fIn.close()
fOut = open("../data/ingestion.p", 'w')
pickle.dump(eing_vals, fOut)
fOut.close()

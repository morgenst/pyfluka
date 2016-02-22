import pickle
import re
from utils import PhysicsQuantities as PQ
from utils import ureg

fIn = open("../data/StSV_Annex3.csv", "r")
LEVals = {}

for line in fIn.readlines()[3:]:
    if not re.match("^[A-Z]", line):
        continue
    line = line.replace('\n', '')
    sl = line.split(',')
    LEVals[PQ.Isotope(int(re.findall(r'\d+', sl[0])[0]), sl[0].split('-')[0], 1 if sl[0].endswith("m") else 0)] = PQ.ExcemptionLimit(float(sl[3]), ureg.Bq/ureg.kg)

fIn.close()
fOut = open("../data/LEDB.p", 'w')
pickle.dump(LEVals, fOut)
fOut.close()

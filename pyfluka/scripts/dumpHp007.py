import pickle

from pyfluka.utils import ureg

from pyfluka.utils.PhysicsQuantities import Isotope, Hp007

fIn = open("../data/Activity_Hp007_conversion.dat", "r")
limits = {}
unit = ureg.Bq / (ureg.mSv / ureg.hour)
for line in fIn:
    line = line.replace("\n", "")
    if line.startswith("#"):
        continue
    sl = line.split()
    try:
        limits[Isotope(abs(int(sl[1])), sl[0], 1 if int(sl[1]) < 0 else 0)] = Hp007(float(sl[2]), unit)
    except ValueError:
        print "FATAL, invalid limit for ", line

fIn.close()
fOut = open("../data/Activity_Hp007_conversion.p", "w")
pickle.dump(limits, fOut)
fOut.close()

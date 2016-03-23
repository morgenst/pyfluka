__author__ = 'marcusmorgenstern'
__mail__ = ''

import pickle
import re
from utils import PhysicsQuantities as PQ
from utils import ureg

f_raw = open("../data/halfLifes.txt", "r")
half_life_vals = {}

str_to_unit = {"s": ureg.second, "h": ureg.hour, "d": ureg.day, "m": ureg.minute, "y": ureg.year}
rg = re.compile("\d+\.?\d*[eE]?[+-]?\d*")
for line in f_raw.readlines()[3:]:
    if not re.match("^[A-Z]", line):
        continue
    line = line.replace('\n', '')
    sl = line.split(' ')
    if "None" not in sl[-1]:
        time = PQ.Time(map(float, rg.findall(sl[-1]))[0], 0., str_to_unit[sl[-1][-1]])
    else:
        #stable isotope
        time = PQ.Time(-1., -1., ureg.year)
    half_life_vals[PQ.Isotope(int(re.findall(r'\d+', sl[0])[0]),
                              sl[0].split('-')[0],
                              1 if sl[0].endswith("M") else 0)] = time

f_raw.close()

f_pickle = open("../data/half_lifes.p", 'w')
pickle.dump(half_life_vals, f_pickle)
f_pickle.close()

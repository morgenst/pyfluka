import pickle
from plugins.BasePlugin import BasePlugin
from utils import PhysicsQuantities as PQ


class TimeEvolution(BasePlugin):
    def __init__(self, config):
        self.config =config
        f_ad = open("../data/timeevolution_ad.p", "r")
        self.data_raw = pickle.load(f_ad)

    def invoke(self, data):
        for det in data.keys():
            self._apply_coefficient(data[det])

    def _apply_coefficient(self, data):
        for k, val in data.iteritems():
            val["ProductionYield"] *= self.data_raw.get(k, 0.)

from plugins.BasePlugin import BasePlugin
from utils import PhysicsQuantities as PQ

class TimeEvolution(BasePlugin):
    def __init__(self, config):
        self.config =config
        self.data_raw = {PQ.Isotope(3, 1, 0): 0.86020262228297506}

    def invoke(self, data):
        for det in data.keys():
            self._apply_coefficient(data[det])

    def _apply_coefficient(self, data):
        for k, val in data.iteritems():
           val["ProductionYield"] *= self.data_raw[k]

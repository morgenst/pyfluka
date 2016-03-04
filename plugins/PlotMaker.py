import importlib
from base import InvalidInputError
from BasePlugin import BasePlugin
from utils.Plotter import Plotter, PlotConfig, packData

class PlotMaker(BasePlugin):
    def __init__(self, config = None, configName = None):
        self.plotter = Plotter()
        if isinstance(config, dict):
            self.config = [PlotConfig(name, c) for name, c in config.items()]
        elif all(isinstance(elem, dict) for elem in config):
            self.config = [PlotConfig(configName, configDict) for configDict in config]
        elif isinstance(config, list) and all(isinstance(elem, PlotConfig) for elem in config):
            self.config = PlotConfig
        else:
            raise InvalidInputError("Unable to parse config from type " + str(type(config)))
        self.plots = {}

    def invoke(self, data):
        self.data = data
        for pc in self.config:
            self.currentPC = pc
            if pc.type == '2D':
                try:
                    self._makePlot2D()
                except Exception as e:
                    raise e

    def _makePlot2D(self):
        m = importlib.import_module("utils.PhysicsQuantities")
        quantity = getattr(m, self.currentPC.quantity)
        for det, fullData in self.data.items():
            try:
                plotData, binning = fullData[self.currentPC.quantity], fullData["Binning"]
                if all(isinstance(elem, quantity) for elem in plotData):
                    plotData = packData(plotData, binning)
            except AttributeError:
                raise AttributeError("Requested quantity " + self.currentPC.quantity + " not calculated.")
            if not det:
                det = ""
            try:
                self.plotter.plotMatrix(plotData[0], binning,
                                        outFileName=self.currentPC.name + det)
            except TypeError:
                raise InvalidInputError("Unable to store plot. Either plot config or detector is unnamed")

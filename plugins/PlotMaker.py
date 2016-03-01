from BasePlugin import BasePlugin
from utils.Plotter import Plotter


class PlotMaker(BasePlugin):
    def __init__(self, config = None):
        self.plotter = Plotter()
        self.config = config
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
        for det, fullData in self.data.items():
            try:
                plotData, binning = fullData[self.currentPC.quantity]
            except AttributeError:
                raise AttributeError("No quantity requested to plot")
            #self.plotter.plotMatrix(plotData, binning)
            plot = None
            try:
                self.plots['2D'].append(plot)
            except KeyError:
                self.plots['2D'] = [plot]
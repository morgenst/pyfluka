import importlib

from BasePlugin import BasePlugin
from pyfluka.base import InvalidInputError
from pyfluka.utils.Plotter import Plotter, PlotConfig, pack_data


class PlotMaker(BasePlugin):
    def __init__(self, config=None, config_name=None):
        """
        Constructor

        :param config: dictionary containing plot config
        :param config_name: (optional) plot specific config in case of multiple configurations in config
        """
        self.data = None
        self.current_plot_config = None
        self.plotter = Plotter()
        if isinstance(config, dict):
            self.config = [PlotConfig(name, c) for name, c in config.items()]
        elif all(isinstance(elem, dict) for elem in config):
            self.config = [PlotConfig(config_name, config_dict) for config_dict in config]
        elif isinstance(config, list) and all(isinstance(elem, PlotConfig) for elem in config):
            self.config = config
        else:
            raise InvalidInputError("Unable to parse config from type " + str(type(config)))
        self.plots = {}

    def invoke(self, data):
        """
        Execution method starting plotting
        :param data: dictionary containing data to be plotted, binning
        :return:
        """
        self.data = data
        for pc in self.config:
            self.current_plot_config = pc
            if pc.type == '2D':
                try:
                    self._make_plot_2d()
                except Exception as e:
                    raise e

    def _make_plot_2d(self):
        m = importlib.import_module("pyfluka.utils.PhysicsQuantities")
        quantity = getattr(m, self.current_plot_config.quantity)
        for det, fullData in self.data.items():
            try:
                plot_data, binning = fullData[self.current_plot_config.quantity], fullData["Binning"]
                if all(isinstance(elem, quantity) for elem in plot_data):
                    plot_data = pack_data(plot_data, binning)
            except AttributeError:
                raise AttributeError("Requested quantity " + self.current_plot_config.quantity + " not calculated.")
            if not det:
                det = ""
            try:
                self.plotter.plot_matrix(plot_data[0], binning,
                                         plot_config=self.current_plot_config,
                                         out_filename=self.current_plot_config.name + det)
            except TypeError:
                raise InvalidInputError("Unable to store plot. Either plot config or detector is unnamed")

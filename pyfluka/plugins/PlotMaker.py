import importlib

import numpy as np
from BasePlugin import BasePlugin
from pyfluka.base import InvalidInputError
from pyfluka.utils.Plotter import Plotter, PlotConfig
from pyfluka.utils.DataTransformations import pack_data


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
            if pc.type.find('projection') > -1:
                try:
                    self._make_projection()
                except Exception as e:
                    raise e

    def _make_projection(self):
        m = importlib.import_module("pyfluka.utils.PhysicsQuantities")
        quantity = getattr(m, self.current_plot_config.quantity)
        projection_axis = self.current_plot_config.type.replace("projection_", "")
        valid_axes = ["x", "y"]
        if projection_axis not in valid_axes:
            raise InvalidInputError("Invalid request of projection axis " + projection_axis)
        if "range" not in self.current_plot_config:
            raise InvalidInputError("Missing range config for " + self.current_plot_config.name)
        projection_axis_index = valid_axes.index(projection_axis)
        projection_range = map(float, self.current_plot_config.range.split(","))
        for det, fullData in self.data.items():
            try:
                plot_data, binning = fullData[self.current_plot_config.quantity], fullData["Binning"]
                binning.reverse()
                if all(isinstance(elem, quantity) for elem in plot_data):
                    plot_data = pack_data(plot_data, binning)
            except AttributeError:
                raise AttributeError("Requested quantity " + self.current_plot_config.quantity + " not calculated.")
            print plot_data[0]
            binning_projection_axis = binning[projection_axis_index]
            slice = None
            if "range" in self.current_plot_config:
                slice = map(int, self.current_plot_config.range.split(','))
                if len(slice) != 2:
                    raise InvalidInputError("Invalid slice request " + str(slice) + ". Range must be two values "
                                                                                    "comma separated")
            if slice:
                a[:, 0:2].sum(axis=1)
                projected_data = plot_data[0].sum(axis=projection_axis_index)
            projected_data = plot_data[0].sum(axis=projection_axis_index)
            print type(projected_data)
            print projected_data
            # self.plotter.plot_projection(plot_data[0], binning,
            #                              projection_axis, self.current_plot_config)

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

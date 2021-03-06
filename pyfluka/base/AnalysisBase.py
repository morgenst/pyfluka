__author__ = 'morgenst'

import importlib
import inspect
import pkgutil
import re

import ConfigParser as CP
import GraphBuilder as GB
from pyfluka import plugins
from pyfluka.base import IllegalArgumentError, InvalidInputError
from pyfluka.reader import UsrbinReader, ResnucReader
from pyfluka.utils.ShellUtils import mkdir


class AnalysisBase:
    def __init__(self, data_file, config_file, output_dir='.'):
        """
        Constructor
        :param data_file (str): input file
        :param config_file (str): configuration file in yaml format
        :param output_dir (Optional[str]): output directory. Defaults to current directory
        :return: void
        """

        self.data_file = data_file
        self.config_file = config_file
        self.output_dir = output_dir
        self._load_plugins()
        self.graph = None
        self.data = None

    def setup(self):
        """
        Setup function to load configuration, build graph to be processed, creates output directory if necessary
        :return:
        """
        self._load_config()
        plugins = self.config['plugins']
        self.graph = GB.build_graph(plugins)
        mkdir(self.output_dir)

    def _load_config(self):
        """
        Loads configuration from input yaml file
        :return:

        Raises:
            IOError: If config file cannot be parsed
        """
        try:
            self.config = CP.parse(self.config_file)
        except IOError as e:
            raise e

    def read_data(self):
        """
        Reads input file and stores data in dict
        :return:
        """
        reader = None
        if self.data_file.lower().count('usrbin'):
            reader = UsrbinReader.UsrbinReader(self.config['storedQuantity'])
        elif self.data_file.lower().count('resnuc'):
            reader = ResnucReader.ResnucReader(self.config['storedQuantity'])
        self.data = reader.load(self.data_file)

    def run(self):
        """
        Executing method called by analysis script.
        :return:
        """
        self.setup()
        self.read_data()
        paths = GB.get_paths(self.graph)
        while True:
            try:
                self.process_path(paths.next())
            except StopIteration:
                break

    def process_path(self, path):
        """
        Processes a single path from graph
        :param path (list): list of plugins to be invoked
        :return:
        """
        for plugin_name in path[1:-1]:
            plugin_base_name = re.sub("_\d+", "", plugin_name)
            if plugin_base_name not in self.plugins.keys():
                raise ValueError("Invalid plugin request " + plugin_name)
            plugin_config = self.graph.node[plugin_name]
            if plugin_config.keys() == ["list_config"]:
                plugin_config = plugin_config["list_config"]
            try:
                plugin = self.plugins[plugin_base_name](plugin_config)
            except (TypeError, IllegalArgumentError, InvalidInputError):
                try:
                    plugin = self.plugins[plugin_base_name](**plugin_config)
                except (TypeError, IllegalArgumentError):
                    raise TypeError("Unable to instantiate plugin %s with %s" % (plugin_base_name, plugin_config))

            plugin.invoke(self.data)

    def _load_plugins(self):
        """
        Parses plugin directory for all available plugins.
        :return:
        """

        package = plugins
        self.plugins = dict()
        for importer, modname, ispkg in pkgutil.walk_packages(path=package.__path__,
                                                              prefix=package.__name__ + '.',
                                                              onerror=lambda x: None):
            m = importlib.import_module(modname)
            self.plugins.update(dict((i[0], i[1])
                                     for i in inspect.getmembers(m, inspect.isclass) if i[1].__module__ == m.__name__))

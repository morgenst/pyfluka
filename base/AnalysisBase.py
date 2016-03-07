__author__ = 'morgenst'

import importlib
import ConfigParser as CP
import GraphBuilder as GB
from utils.ShellUtils import mkdir
from reader import UsrbinReader, ResnucReader
import inspect
import importlib
import pkgutil
import plugins


class AnalysisBase:
    def __init__(self, dataFile, configFile, outputDir = '.'):
        """
        Constructor
        :param dataFile (str): input file
        :param configFile (str): configuration file in yaml format
        :param outputDir (Optional[str]): output directory. Defaults to current directory
        :return: void
        """

        self.dataFile = dataFile
        self.configFile = configFile
        self.outputDir = outputDir
        self._load_plugins()
        self.graph = None
        self.data = None

    def setup(self):
        """
        Setup function to load configuration, build graph to be processed, creates output directory if necessary
        :return:
        """
        self._loadConfig()
        plugins = self.config['plugins']
        self.graph = GB.build_graph(plugins)
        mkdir(self.outputDir)

    def _loadConfig(self):
        """
        Loads configuration from input yaml file
        :return:

        Raises:
            IOError: If config file cannot be parsed
        """
        try:
            self.config = CP.parse(self.configFile)
        except IOError as e:
            raise e

    def read_data(self):
        """
        Reads input file and stores data in dict
        :return:
        """
        reader = None
        if self.dataFile.lower().count('usrbin'):
            reader = UsrbinReader.UsrbinReader(self.config['storedQuantity'])
        elif self.dataFile.lower().count('resnuc'):
            reader = ResnucReader.ResnucReader()
        self.data = reader.load(self.dataFile)

    def run(self):
        """
        Executing method called by analysis script.
        :return:
        """
        self.setup()
        self.read_data()
        paths = GB.getPaths(self.graph)
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
        for pluginName in path[1:-1]:
            if pluginName not in self.plugins.keys():
                raise ValueError("Invalid plugin request " + pluginName)
            plugin_config = self.graph.node[pluginName]
            plugin = self.plugins[pluginName](plugin_config)
            plugin.invoke(self.data)

    def _load_plugins(self):
        """
        Parses plugin directory for all available plugins.
        :return:
        """
        package = plugins
        self.plugins = dict()
        for importer, modname, ispkg in pkgutil.walk_packages(path=package.__path__,
                                                              prefix=package.__name__+'.',
                                                              onerror=lambda x: None):
            m = importlib.import_module(modname)
            self.plugins.update(dict((i[0], i[1]) for i in inspect.getmembers(m, inspect.isclass) if i[1].__module__ == m.__name__))

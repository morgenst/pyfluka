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
        self.dataFile = dataFile
        self.configFile = configFile
        self.outputDir = outputDir
        self._loadPlugins()

    def setup(self):
        self._loadConfig()
        plugins = self.config['plugins']
        self.graph = GB.build_graph(plugins)
        mkdir(self.outputDir)

    def _loadConfig(self):
        try:
            self.config = CP.parse(self.configFile)
        except IOError as e:
            raise e

    def readData(self):
        reader = None
        if self.dataFile.lower().count('usrbin'):
            reader = UsrbinReader.UsrbinReader(self.config['storedQuantity'])
        elif self.dataFile.lower().count('resnuc'):
            reader = ResnucReader.ResnucReader()
        self.data = reader.load(self.dataFile)


    def run(self):
        self.setup()
        self.readData()
        paths = GB.getPaths(self.graph)
        while True:
            try:
                self.processPath(paths.next())
            except StopIteration:
                break

    def processPath(self, path):
        for pluginName in path[1:-1]:
            if pluginName not in self.plugins.keys():
                raise ValueError("Invalid plugin request " + pluginName)
            pluginConfig = self.graph.node[pluginName]
            plugin = self.plugins[pluginName](pluginConfig)
            plugin.invoke(self.data)
            #plugin = getattr(m, pluginName)
            #plugin.invoke(self.data)


    def _loadPlugins(self):
        package = plugins
        self.plugins = dict()
        for importer, modname, ispkg in pkgutil.walk_packages(path=package.__path__,
                                                      prefix=package.__name__+'.',
                                                      onerror=lambda x: None):

            m = importlib.import_module(modname)
            self.plugins.update(dict((i[0], i[1]) for i in inspect.getmembers(m, inspect.isclass) if i[1].__module__ == m.__name__))

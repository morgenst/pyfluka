__author__ = 'morgenst'

import ConfigParser as CP
import GraphBuilder as GB
from utils.ShellUtils import mkdir
from reader import UsrbinReader, ResnucReader


class AnalysisBase:
    def __init__(self, dataFile, configFile, outputDir = '.'):
        self.dataFile = dataFile
        self.configFile = configFile
        self.outputDir = outputDir

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
        if self.dataFile.count('usrbin'):
            reader = UsrbinReader(self.config['storedQuantity'])
        elif self.dataFile.count('resnuc'):
            reader = ResnucReader()
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
        print path



__author__ = 'morgenst'

import ConfigParser as CP
import GraphBuilder as GB

class BaseCycle:
    def __init__(self, configFile):
        self.configFile = configFile

    def setup(self):
        self._loadConfig()

        plugins = self.config['plugins']
        #self.graph = GB.build_graph(plugins.keys())


    def _loadConfig(self):
        try:
            self.config = CP.parse(self.configFile)
        except IOError as e:
            raise e

    def run(self):
        pass


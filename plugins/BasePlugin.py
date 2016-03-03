__author__ = 'marcusmorgenstern'
__mail__ = ''

from abc import ABCMeta, abstractmethod


class BasePlugin():
    __metaclass__ = ABCMeta

    def __init__(self, config = None):
        self.dep = []

    @abstractmethod
    def invoke(self):
        pass


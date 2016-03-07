__author__ = 'marcusmorgenstern'
__mail__ = ''

from abc import ABCMeta, abstractmethod


class BasePlugin():
    """
    Metaclass for guarantee of interface. Each plugin must provide initialisation taking optional configuration
    and invoke method taking data
    """

    __metaclass__ = ABCMeta

    def __init__(self, config = None):
        """
        initialisation
        :param config (dict): configuration params for plugin
        :return: void
        """
        self.dep = []

    @abstractmethod
    def invoke(self, data):
        """
        Entry for plugin execution
        :param data (dict): input data
        :return: void
        """
        pass


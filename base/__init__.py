__author__ = 'marcusmorgenstern'
__mail__ = ''

from StoredData import GlobalData


class IllegalArgumentError(ValueError):
    pass


class InvalidInputError(ValueError):
    pass

_global_data = GlobalData()

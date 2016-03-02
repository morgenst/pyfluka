__author__ = 'marcusmorgenstern'
__mail__ = ''

from base import IllegalArgumentError
from utils.OrderedYAMLExtension import load, dump


def parse(config):
    try:
        f = open(config)
    except IOError:
        raise IOError('Config file %s does not exist.' % config)
    cDict = load(f)
    try:
        _validate(cDict)
    except Exception as e:
        raise e
    return cDict

def _validate(cDict):
    if not cDict.has_key('plugins'):
        raise IllegalArgumentError("No plugins defined.")
    if not type(cDict['plugins']) is type({}):
        raise IllegalArgumentError("Plugins are required to be dictionaries, but " + str(type(cDict['plugins'])) + " given.")
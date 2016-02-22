__author__ = 'marcusmorgenstern'
__mail__ = ''

from utils.OrderedYAMLExtension import load, dump

def parse(config):
    try:
        f = open(config)
    except IOError:
        raise IOError('Config file %s does not exist.' % config)
    cDict = load(f)
    return cDict
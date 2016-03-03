__author__ = 'marcusmorgenstern'
__mail__ = ''

from base import IllegalArgumentError
from utils.OrderedYAMLExtension import load, dump
import utils.PhysicsQuantities as PQ
from utils import ureg


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
    _transform(cDict)
    return cDict


def _validate(cDict):
    if not cDict.has_key('plugins'):
        raise IllegalArgumentError("No plugins defined.")
    if not type(cDict['plugins']) is type({}):
        raise IllegalArgumentError("Plugins are required to be dictionaries, but " + str(type(cDict['plugins'])) + " given.")


def _transform(config):
    if config.has_key("detectors"):
        _transformDetInfo(config["detectors"])

def _transformDetInfo(config):
    for det in config.keys():
        for quantity, val in config[det].items():
            if quantity.lower() == 'mass':
                info = val.split(' ')
                config[det][quantity] = PQ.Mass(float(info[0]), ureg(info[1]))

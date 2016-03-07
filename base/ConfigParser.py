__author__ = 'marcusmorgenstern'
__mail__ = ''

import yaml
import yamlordereddictloader
import utils.PhysicsQuantities as PQ
from base import IllegalArgumentError
from utils import ureg
from collections import OrderedDict


def parse(config):
    try:
        f = open(config)
    except IOError:
        raise IOError('Config file %s does not exist.' % config)
    cDict = yaml.load(f, Loader=yamlordereddictloader.Loader)
    try:
        _validate(cDict)
    except Exception as e:
        raise e
    _transform(cDict)
    return cDict


def _validate(cDict):
    if 'plugins' not in cDict:
        raise IllegalArgumentError("No plugins defined.")
    if not isinstance(cDict['plugins'], OrderedDict):
        raise IllegalArgumentError("Plugins are required to be dictionaries, but " + str(type(cDict['plugins'])) +
                                   " given.")


def _transform(config):
    if "detectors" in config:
        _transformDetInfo(config["detectors"])


def _transformDetInfo(config):
    for det in config.keys():
        for quantity, val in config[det].items():
            if quantity.lower() == 'mass':
                info = val.split(' ')
                config[det][quantity] = PQ.Mass(float(info[0]), ureg(info[1]))

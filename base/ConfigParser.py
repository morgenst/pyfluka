__author__ = 'marcusmorgenstern'
__mail__ = ''

import yaml
import yamlordereddictloader
import utils.PhysicsQuantities as PQ
from base import IllegalArgumentError, _global_data
from utils import ureg
from collections import OrderedDict


def parse(config):
    try:
        f = open(config)
    except IOError:
        raise IOError('Config file %s does not exist.' % config)
    config_dict = yaml.load(f, Loader=yamlordereddictloader.Loader)
    try:
        _validate(config_dict)
    except Exception as e:
        raise e
    _transform(config_dict)
    return config_dict


def _validate(config_dict):
    if 'plugins' not in config_dict:
        raise IllegalArgumentError("No plugins defined.")
    if not isinstance(config_dict['plugins'], OrderedDict):
        raise IllegalArgumentError("Plugins are required to be dictionaries, but " + str(type(config_dict['plugins'])) +
                                   " given.")


def _transform(config):
    if "detectors" in config:
        _transform_det_info(config.pop("detectors"))


def _transform_det_info(config):
    for det in config.keys():
        for quantity, val in config[det].items():
            if quantity.lower() == 'mass':
                info = val.split(' ')
                _global_data.add(det, quantity, PQ.Mass(float(info[0]), info[1]))

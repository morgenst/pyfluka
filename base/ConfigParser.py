__author__ = 'marcusmorgenstern'
__mail__ = ''

import yaml
import yamlordereddictloader
import utils.PhysicsQuantities as PQ
from base import IllegalArgumentError, _global_data
from collections import OrderedDict


def parse(config):
    """
    Parsing function
    :param config (str): filename of config file
    :return (dict): configuration as dict

    Raises:
        IOError: if config file does not exist
        IllegalArgument: if validation fails; see _validate
    """
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
    """
    Validates configuration w.r.t required information, i.e. plugins have to be defined, and checks for compliance
    of data structure
    :param config_dict (dict): parsed configuration dictionary
    :return:

    Raises:
        IllegealArgumentError: if any validation check fails
    """
    if 'plugins' not in config_dict:
        raise IllegalArgumentError("No plugins defined.")
    if not isinstance(config_dict['plugins'], OrderedDict):
        raise IllegalArgumentError("Plugins are required to be dictionaries, but " + str(type(config_dict['plugins'])) +
                                   " given.")


def _transform(config):
    """
    Executes transformation steps
    :param config (dict): parsed configuration dictionary
    :return:
    """
    if "detectors" in config:
        _transform_det_info(config.pop("detectors"))
    if "global" in config:
        _set_global_data(config.pop("global"))


def _transform_det_info(config):
    """
    Transform parsed detector information
    :param config (dict): parsed configuration dictionary
    :return:
    """
    for det in config.keys():
        for quantity, val in config[det].items():
            if quantity.lower() == 'mass':
                info = val.split(' ')
                _global_data.add(det, quantity, PQ.Mass(float(info[0]), info[1]))


def _set_global_data(config):
    for k, v in config.iteritems():
        _global_data.add(k, v)


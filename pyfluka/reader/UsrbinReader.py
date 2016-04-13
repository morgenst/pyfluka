import operator
from functools import partial
from itertools import chain

import numpy as np

from BaseReader import BaseReader
from pyfluka.base import InvalidInputError


class UsrbinReader(BaseReader):
    def __init__(self, quantity="Activity", dim=None, weights=None):
        super(self.__class__, self).__init__(quantity, dim, weights)

    def _load(self, filename, weight):
        """
        Incorporate search for "this is" to detect line above the first line and "error" to detect end of value block
        """

        def pack_data(dataraw, axesdata):
            try:
                bin_shape = (axesdata[0][2], axesdata[1][2], axesdata[2][2])  # x,y,z
            except:
                bin_shape = (axesdata[0][2], axesdata[1][2])  # x,y,z
            reverse_bin_shape = list(bin_shape)
            reverse_bin_shape.reverse()
            dataraw = [self.pq(v, unit=self.dim) if hasattr(self, 'dim') else self.pq(v) for v in dataraw]
            try:
                return np.reshape(np.array(dataraw), reverse_bin_shape).transpose()
            except:
                return np.reshape(np.array(dataraw[:-1]), reverse_bin_shape).transpose()

        usrbin_data_dict = {}
        current_detector_name = None
        data = []
        axesdata = []

        primaries_weight_info = None
        data_reached = False
        error_mode = False

        for (i, line) in enumerate(file(filename)):
            if line.find("error") > 0:
                error_mode = True
            if line.find("Total number of particles followed") > 0:
                linesplit = line.split()
                primaries_weight_info = (float(linesplit[5][:-1]), float(linesplit[11]))

            if line.find("binning n.") > 0:
                error_mode = False
                if current_detector_name is not None:
                    usrbin_data = pack_data(data, axesdata)
                    usrbin_data_dict[current_detector_name] = (usrbin_data, axesdata, primaries_weight_info)
                    current_detector_name = None
                    data = []
                    axesdata = []
                    data_reached = False
                    error_mode = False
                    primaries_weight_info = None
                current_detector_name = line.split("\"")[1].strip()

            if data_reached and not error_mode:
                data_line = [x for x in map(float, line.split())]
                if data_line:
                    data.append(data_line)
            else:
                if line.find("coordinate:") > 0:
                    splitted = line.split()
                    axis_data = (splitted[3], splitted[5], splitted[7])
                    axesdata.append((float(splitted[3]), float(splitted[5]), int(splitted[7])))
                if line.find("this is") > 0 or line.find("accurate deposition") > 0:
                    data_reached = True
        data = list(chain.from_iterable(data))
        usrbin_data = pack_data(data, axesdata)
        usrbin_data *= weight
        primaries_weight_info = tuple(map(partial(operator.mul, weight), primaries_weight_info))
        usrbin_data_dict[current_detector_name] = {self.pq.__name__: usrbin_data,
                                                   "Binning": axesdata,
                                                   "Weight": primaries_weight_info}
        return usrbin_data_dict

    @staticmethod
    def get_axis_index(axisdata, value):
        start, end, nbins = axisdata
        step = (end - start) / nbins
        if value < start:
            return -1
        if value > end:
            return nbins
        return int((value - start) / step)

    @staticmethod
    def _merge(merged_data, data):

        def _validate_merge(merged_data, data):
            if not merged_data["Binning"] == data["Binning"]:
                raise InvalidInputError("Requested merging with inconsistent binning: " +
                                        str(merged_data["Binning"]) + " and " + str(data["Binning"]))

        for det in data.keys():
            keys = data[det].keys()
            keys.remove("Binning")
            try:
                _validate_merge(merged_data[det], data[det])
            except Exception as e:
                raise e
            for key in keys:
                if isinstance(data[det][key], tuple):
                    merged_data[det][key] = tuple(map(operator.add, merged_data[det][key], data[det][key]))
                elif isinstance(data[det][key], np.ndarray):
                    merged_data[det][key] += data[det][key]
                else:
                    raise InvalidInputError("Request merge for unsupported type " + type(data[det][key]))

import copy
from collections import OrderedDict

import pyfluka.utils.PhysicsQuantities as PQ
from BaseReader import BaseReader
from pyfluka.base.StoredData import StoredData


class ResnucReader(BaseReader):
    def __init__(self, quantity="Activity", dim=None, weights=None):
        super(self.__class__, self).__init__(quantity, dim, weights)

    def _load(self, filename, weight):
        resnucl_data_dict = {}
        first_line_of_detector = False
        data_section = False
        isomere_section = False
        current_detector_name = None
        data = OrderedDict()

        for (i, line) in enumerate(file(filename)):
            if line.find("Detector n:") > 0:
                first_line_of_detector = True
                data_section = False
                isomere_section = False
            elif line.find("A/Z Isotopes:") > 0:
                first_line_of_detector = False
                data_section = True
                isomere_section = False
            elif line.find("A/Z/m Isomers:") > 0:
                first_line_of_detector = False
                data_section = False
                isomere_section = True
            elif first_line_of_detector:
                if current_detector_name is not None:
                    resnucl_data_dict[current_detector_name] = copy.copy(data)
                    current_detector_name = None
                    data = {}
                current_detector_name = line.strip()
                first_line_of_detector = False
            elif data_section:
                split_line = line.split()
                A = split_line[0]
                Z = int(split_line[1])
                value = weight * float(split_line[2])
                error_percent = float(split_line[3])
                if value > 0.:
                    try:
                        data[PQ.Isotope(A, Z, 0)].append(self.pq(value, unc=value * error_percent / 100.))
                    except KeyError:
                        data[PQ.Isotope(A, Z, 0)] = StoredData(self.pq(value, unc=value * error_percent / 100.))
            elif isomere_section:
                split_line = line.split()
                if not len(split_line):
                    continue
                A = split_line[0]
                Z = int(split_line[1])
                iso = int(split_line[2])
                value = weight * float(split_line[3])
                error_percent = float(split_line[4])
                if value > 0.:
                    try:
                        data[PQ.Isotope(A, Z, iso)].append(self.pq(value, unc=value * error_percent / 100.))
                    except KeyError:
                        data[PQ.Isotope(A, Z, iso)] = StoredData(self.pq(value, unc=value * error_percent / 100.))

        if current_detector_name is not None:
            resnucl_data_dict[current_detector_name] = copy.copy(data)

        return resnucl_data_dict

    @staticmethod
    def _merge(res, addend):
        for det in res.keys():
            all_isotopes = list(set(res[det].keys()) | set(addend[det].keys()))
            for isotope in all_isotopes:
                res[det][isotope] += (addend[det][isotope])



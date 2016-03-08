import copy
from utils.PhysicsQuantities import Isotope, Activity


class ResnucReader:
    def __init__(self):
        pass

    @staticmethod
    def load(filename):
        resnucl_data_dict = {}
        first_line_of_detector = False
        data_section = False
        isomere_section = False
        current_detector_name = None
        data = {'Isotope': [], 'Activity': []}

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
                    data = {'Isotope': [], 'Activity': []}
                current_detector_name = line.strip()
                first_line_of_detector = False
            elif data_section:
                split_line = line.split()
                A = split_line[0]
                Z = int(split_line[1])
                value = float(split_line[2])
                error_percent = float(split_line[3])
                if value > 0.:
                    data['Isotope'].append(Isotope(A, Z, 0))
                    data['Activity'].append(Activity(value, unc=value * error_percent / 100.))
            elif isomere_section:
                split_line = line.split()
                if not len(split_line):
                    continue
                A = split_line[0]
                Z = int(split_line[1])
                iso = int(split_line[2])
                value = float(split_line[3])
                error_percent = float(split_line[4])
                if value > 0.:
                    data['Isotope'].append(Isotope(A, Z, iso))
                    data['Activity'].append(Activity(value, unc=value * error_percent / 100.))

        if current_detector_name is not None:
            resnucl_data_dict[current_detector_name] = copy.copy(data)

        return resnucl_data_dict

    def read_single_detector(self):
        pass


import copy
from utils.PhysicsQuantities import Isotope, Activity


class ResnucReader:
    def __init__(self):
        pass

    def load(self, filename):
        resnuclDataDict = {}
        FirstLineOfDetector = False
        DataSection = False
        IsomereSection = False
        currentDetectorName = None
        data = {'Isotope': [], 'Activity': []}

        for (i, line) in enumerate(file(filename)):
            if line.find("Detector n:") > 0:
                FirstLineOfDetector = True
                DataSection = False
                IsomereSection = False
            elif line.find("A/Z Isotopes:") > 0:
                FirstLineOfDetector = False
                DataSection = True
                IsomereSection = False
            elif line.find("A/Z/m Isomers:") > 0:
                FirstLineOfDetector = False
                DataSection = False
                IsomereSection = True
            elif FirstLineOfDetector:
                if currentDetectorName is not None:
                    resnuclDataDict[currentDetectorName] = copy.copy(data)
                    currentDetectorName = None
                    data = {}
                currentDetectorName = line.strip()
                FirstLineOfDetector = False
            elif DataSection:
                splitLine = line.split()
                A = splitLine[0]
                Z = int(splitLine[1])
                value = float(splitLine[2])
                errorPercent = float(splitLine[3])
                if value > 0.:
                    data['Isotope'].append(Isotope(A, Z, 0))
                    data['Activity'].append(Activity(value, unc=value * errorPercent / 100.))
            elif IsomereSection:
                splitLine = line.split()
                A = splitLine[0]
                Z = int(splitLine[1])
                iso = int(splitLine[2])
                value = float(splitLine[3])
                errorPercent = float(splitLine[4])
                if value > 0.:
                    data['Isotope'].append(Isotope(A, Z, iso))
                    data['Activity'].append(Activity(value, unc=value * errorPercent / 100.))

        if currentDetectorName is not None:
            resnuclDataDict[currentDetectorName] = copy.copy(data)

        return resnuclDataDict



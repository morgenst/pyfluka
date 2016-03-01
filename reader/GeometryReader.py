import copy


class GeometryReader(object):
    def __init__(self):
        pass

    def loadGeometryFile(self, filename, firstIndex=2, lastIndex=4):
        """ Reads in a geometry file from FLUKA
        x Axis -> Index 2
        y Axis -> Index 3
        z Axis -> Index 4
        Default: x and z Axis
        """
        X = []
        Y = []
        Xs = []
        Ys = []
        for line in file(filename):
            if line[0] == "#":
                continue
            if line.strip() == "":
                if X:
                    Xs.append(copy.copy(X))
                    Ys.append(copy.copy(Y))

                    X = []
                    Y = []
            else:
                try:
                    splitted = map(float, line.split())
                    if len(splitted) == 5:
                        X.append(splitted[firstIndex])
                        Y.append(splitted[lastIndex])
                except:
                    pass
        if X:
            Xs.append(copy.copy(X))
            Ys.append(copy.copy(Y))
            X = []
            Y = []

        return Xs, Ys

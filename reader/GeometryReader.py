import copy


class GeometryReader(object):
    def __init__(self):
        pass

    def load_geometry_file(self, filename, first_index=2, last_index=4):
        """ Reads in a geometry file from FLUKA
        x Axis -> Index 2
        y Axis -> Index 3
        z Axis -> Index 4
        Default: x and z Axis
        """
        x = []
        y = []
        xs = []
        ys = []
        for line in file(filename):
            if line[0] == "#":
                continue
            if line.strip() == "":
                if x:
                    xs.append(copy.copy(x))
                    ys.append(copy.copy(y))

                    x = []
                    y = []
            else:
                try:
                    splitted = map(float, line.split())
                    if len(splitted) == 5:
                        x.append(splitted[first_index])
                        y.append(splitted[last_index])
                except:
                    pass
        if x:
            xs.append(copy.copy(x))
            ys.append(copy.copy(y))
            x = []
            y = []

        return xs, ys

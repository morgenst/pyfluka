import copy
from base import InvalidInputError

class GeometryReader(object):
    def __init__(self):
        self.axis_indices = {"x": 2, "y": 3, "z": 4}

    def load(self, filename, first_index="x", last_index="z"):
        """
        Reads in a geometry file from FLUKA
        :param filename (str): input filename
        :param first_index (str): first axis, defaults to x axis
        :param last_index (str):  second axis, default to y axis
        :return:
        """
        if first_index not in self.axis_indices.keys() or last_index not in self.axis_indices.keys():
            raise InvalidInputError("Invalid axis indices. Must be either x, y or z, but given " + first_index +
                                    " and " + last_index)
        first_index = self.axis_indices[first_index]
        last_index = self.axis_indices[last_index]
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
                except Exception as e:
                    pass
        if x:
            xs.append(copy.copy(x))
            ys.append(copy.copy(y))
            x = []
            y = []
        return xs, ys

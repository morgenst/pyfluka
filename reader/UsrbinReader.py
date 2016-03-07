import copy
import importlib
import pylab
import numpy as np
from functools import partial
from utils import ureg
from matplotlib.colors import LogNorm, Normalize
from itertools import izip, chain


class UsrbinReader(object):
    def __init__(self, quantity, dim=None):
        m = importlib.import_module("utils.PhysicsQuantities")
        if dim is not None:
            self.dim = ureg(dim)
        self.pq = getattr(m, quantity)

    def load(self, filename):
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
                if data_line != []:
                    data.append(data_line)
            else:
                if line.find("coordinate:") > 0:
                    splitted = line.split()
                    axis_data = (splitted[3], splitted[5], splitted[7])
                    axesdata.append((float(splitted[3]), float(splitted[5]), int(splitted[7])))
                if line.find("this is") > 0:
                    data_reached = True
        data = list(chain.from_iterable(data))
        usrbin_data = pack_data(data, axesdata)

        usrbin_data_dict[current_detector_name] = {self.pq.__name__: usrbin_data,
                                                   "Binning": axesdata,
                                                   "Weight": primaries_weight_info}
        return usrbin_data_dict

    def get_axis_index(self, axisdata, value):
        start, end, nbins = axisdata
        step = (end - start) / nbins
        if value < start:
            return -1
        if value > end:
            return nbins
        return int((value - start) / step)

    """

    def getValue(self, x, y, z, data, axesdata):
        xIndex = getAxisIndex(axesdata[0], x)

        yIndex = getAxisIndex(axesdata[1], y)
        zIndex = getAxisIndex(axesdata[2], z)
        # print xIndex, yIndex, zIndex
        return data[xIndex, yIndex, zIndex]


    if __name__ == "__main__":

        import os
        filename = os.environ.get('PYTHONSTARTUP')
        if filename and os.path.isfile(filename):
            execfile(filename)

        from pydoc import help
        from pprint import pprint

        usrbinDataDict = load(sys.argv[1])
        # BinShape = (axesdata[0][2],axesdata[1][2],axesdata[2][2]) # x,y,z

        # ReverseBinShape = list(BinShape)
        # ReverseBinShape.reverse()
        # a = np.array(data)
        # b = np.reshape(a, (150,30, -1))
        # usrbin_data = np.reshape(np.array(data),ReverseBinShape).transpose()

        if False:
            normalizationFactor = 1E-12 * 8.34E12 * 3600 * 1E6

            # plotMatrix(usrbin_data[75,:,:].transpose(), axesdata[1:])
            plotMatrixShort(usrbin_data, axesdata, (Ellipsis, 15, Ellipsis), transpose=True,
                            geometryData=loadGeometryFile(sys.argv[2]), savefilename="plot.pdf")

            # print getAxesRange(axesdata[0])



            # print normalizationFactor * getValue(800,0.,44400, usrbin_data, axesdata)

            def myfunc(x):
                if np.isnan(x):
                    return 0.
                else:
                    return x

            vfunc = np.vectorize(myfunc)

            da = usrbin_data * normalizationFactor / (usrbin_data * normalizationFactor / 5.)

            plotMatrixShort(vfunc(da), axesdata, (Ellipsis, 15, Ellipsis), transpose=True, vMin=1e-1, UseLog=False,
                            geometryData=loadGeometryFile(sys.argv[2]))
    """
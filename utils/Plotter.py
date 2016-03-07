import numpy as np
import os.path
from itertools import izip
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm, Normalize


def getAxesRange(axisdata):
    start, end, nBins = axisdata
    step = (end - start) / nBins
    print start, end, nBins, step
    return np.arange(start, end + step / 2., step)


# todo: duplicate of definition in UsrbinReader
def packData(dataraw, axesdata):
    try:
        BinShape = (axesdata[0][2], axesdata[1][2], axesdata[2][2])  # x,y,z
    except:
        BinShape = (axesdata[0][2], axesdata[1][2])  # x,y,z
    ReverseBinShape = list(BinShape)
    ReverseBinShape.reverse()
    try:
        return np.reshape(np.array(dataraw), ReverseBinShape).transpose()
    except:
        return np.reshape(np.array(dataraw[:-1]), ReverseBinShape).transpose()


class Plotter(object):
    def __init__(self, output_dir=".", format="png"):
        """
        Constructor
        :param output_dir (Optional[str]): Output directory. Defaults to current directory.
        :param format: (Optional[str]): File format plots are stored. Defaults to png.
        :return:
        """
        self.outputDir = output_dir
        self.format = format

    def plotMatrix(self, mat, axesdata,
                   out_filename=None,
                   use_log=True,
                   vmin_log=None,
                   vmax_log=None,
                   aspect_ratio_equal=True,
                   geometry_data=None,
                   vmin=None,
                   vmax=None):
        X = getAxesRange(axesdata[2])
        Y = getAxesRange(axesdata[1])
        if use_log:
            plt.pcolor(X, Y, mat.astype(float), norm=LogNorm(vmin=vmin_log, vmax=vmax_log))
        else:
            plt.pcolor(X, Y, mat[0], norm=Normalize(vmin=vmin, vmax=vmax))
        plt.xlim(axesdata[0][0], axesdata[0][1])
        plt.ylim(axesdata[1][0], axesdata[1][1])
        if aspect_ratio_equal:
            plt.axes().set_aspect('equal')
        if geometry_data is not None:
            for x, y in izip(*geometry_data):
                plt.plot(x, y, 'k-', linewidth=2)
        if out_filename:
            plt.savefig(os.path.join(self.outputDir, out_filename), format=self.format)
        return plt

    def plotMatrixShort(self, data, axesdata, selection, transpose=False, UseLog=True, vMinLog=None, vMaxLog=None,
                        aspectRatioEqual=True, geometryData=None, savefilename=None, vMin=None, vMax=None):
        selecteddata = data[selection]
        selectedaxesdata = [axesdata[i] for (i, selectionItem) in enumerate(selection) if selectionItem == Ellipsis]
        print selectedaxesdata
        if transpose:
            selecteddata = selecteddata.transpose()
        else:
            selectedaxesdata.reverse()
        return self.plotMatrix(selecteddata, selectedaxesdata, UseLog, vMinLog, vMaxLog, aspectRatioEqual, geometryData,
                               savefilename, vmin=vMin, vmax=vMax)


class PlotConfig(object):
    def __init__(self, name, kwargs):
        self.name = name
        for attr, val in kwargs.items():
            self.__setattr__(attr, val)

    def __eq__(self, other):
        lhs = {(k, v) for k, v in self.__dict__.items() if not k == 'name'}
        rhs = {(k, v) for k, v in other.__dict__.items() if not k == 'name'}
        return lhs == rhs

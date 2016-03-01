from matplotlib import pyplot as plt
import numpy as np
from matplotlib.colors import LogNorm, Normalize


def getAxesRange(axisdata):
    start, end, nBins = axisdata
    step = (end - start) / nBins
    print start, end, nBins, step
    return np.arange(start, end + step / 2., step)


class Plotter(object):
    def __init__(self):
        pass

    def plotMatrix(self, mat, axesdata,
                   UseLog=True,
                   vMinLog=None,
                   vMaxLog=None,
                   aspectRatioEqual=True,
                   geometryData=None,
                   vMin=None,
                   vMax=None):
        X = getAxesRange(axesdata[2])
        Y = getAxesRange(axesdata[1])
        if UseLog:
            plt.pcolor(X, Y, mat.astype(float), norm=LogNorm(vmin=vMinLog, vmax=vMaxLog))
        else:
            plt.pcolor(X, Y, mat[0], norm=Normalize(vmin=vMin, vmax=vMax))
        # pylab.colorbar()
        plt.xlim(axesdata[0][0], axesdata[0][1])
        plt.ylim(axesdata[1][0], axesdata[1][1])
        if aspectRatioEqual:
            plt.axes().set_aspect('equal')
        if geometryData != None:
            for x, y in izip(*geometryData):
                plt.plot(x, y, 'k-', linewidth=2)
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
                               savefilename, vMin=vMin, vMax=vMax)


class PlotConfig(object):
    def __init__(self, kwargs):
        for attr, val in kwargs.items():
            self.__setattr__(attr, val)
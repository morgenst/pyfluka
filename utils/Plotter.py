import numpy as np
import os.path
from itertools import izip
from matplotlib import pyplot as plt
from matplotlib.colors import LogNorm, Normalize


def get_axes_range(axisdata):
    start, end, nbins = axisdata
    step = (end - start) / nbins
    print start, end, nbins, step
    return np.arange(start, end + step / 2., step)


# todo: duplicate of definition in UsrbinReader
def pack_data(dataraw, axesdata):
    try:
        bin_shape = (axesdata[0][2], axesdata[1][2], axesdata[2][2])  # x,y,z
    except:
        bin_shape = (axesdata[0][2], axesdata[1][2])  # x,y,z
    reverse_bin_shape = list(bin_shape)
    reverse_bin_shape.reverse()
    try:
        return np.reshape(np.array(dataraw), reverse_bin_shape).transpose()
    except:
        return np.reshape(np.array(dataraw[:-1]), reverse_bin_shape).transpose()


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

    def plot_matrix(self, mat, axesdata,
                    out_filename=None,
                    use_log=True,
                    vmin_log=None,
                    vmax_log=None,
                    aspect_ratio_equal=True,
                    geometry_data=None,
                    vmin=None,
                    vmax=None):
        x = get_axes_range(axesdata[2])
        y = get_axes_range(axesdata[1])
        if use_log:
            plt.pcolor(x, y, mat.astype(float), norm=LogNorm(vmin=vmin_log, vmax=vmax_log))
        else:
            plt.pcolor(x, y, mat[0], norm=Normalize(vmin=vmin, vmax=vmax))
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

    def plot_matrix_short(self, data, axesdata, selection, transpose=False, use_log=True, vmin_log=None, vmax_log=None,
                          aspect_ratio_equal=True, geometry_data=None, savefilename=None, vmin=None, vmax=None):
        selecteddata = data[selection]
        selectedaxesdata = [axesdata[i] for (i, selectionItem) in enumerate(selection) if selectionItem == Ellipsis]
        print selectedaxesdata
        if transpose:
            selecteddata = selecteddata.transpose()
        else:
            selectedaxesdata.reverse()
        return self.plot_matrix(selecteddata, selectedaxesdata, use_log, vmin_log, vmax_log, aspect_ratio_equal,
                                geometry_data, savefilename, vmin=vmin, vmax=vmax)


class PlotConfig(object):
    def __init__(self, name, kwargs):
        self.name = name
        for attr, val in kwargs.items():
            self.__setattr__(attr, val)

    def __eq__(self, other):
        lhs = {(k, v) for k, v in self.__dict__.items() if not k == 'name'}
        rhs = {(k, v) for k, v in other.__dict__.items() if not k == 'name'}
        return lhs == rhs

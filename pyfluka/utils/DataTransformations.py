import numpy as np


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

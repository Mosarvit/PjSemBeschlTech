import math
from copy import copy
from helpers.plot_helper import plot_K1
import numpy as np


from helpers.signal_helper import find_nearest


def create_mock_K(points, linearVpp_in_mV, x_range_in_mV, periods) :



    n = int(np.floor(points/2))

    K_pos = np.zeros([n,2])
    K_pos[:,0] = np.linspace(0, x_range_in_mV/2, n)

    ind = find_nearest(K_pos[:,0], linearVpp_in_mV/2)

    K_pos[:, 1][:ind+1] = K_pos[:,0][:ind+1]

    diff = (x_range_in_mV-linearVpp_in_mV)/2

    a = np.sin(np.linspace(0,math.pi*2*periods, K_pos.shape[0]-ind))

    K_pos[:, 1][ind:] =a*diff/math.pi/periods/2 + K_pos[ind, 1]

    K_neg = -np.fliplr([K_pos])[0]

    K = np.concatenate((K_neg[:-1,:], K_pos), axis=0)

    return K


def invert_K(K):

    K_flipped = copy(K)
    K_flipped[:,0] = K[:,1]
    K_flipped[:, 1] = K[:, 0]

    return K_flipped

#
# K = create_mock_K(points=999, linearVpp_in_mV=300, x_range_in_mV=1200, periods=1)
# K_flipped = invert_K(K)
#
# plot_K1(K)
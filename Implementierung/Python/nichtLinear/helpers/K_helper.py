from unittest import TestCase
import unittest
import numpy as np
from numpy import genfromtxt
from scipy import linalg
import matplotlib.pyplot as plt
from blocks.adjust_H import adjust_H
from blocks.adjust_a import adjust_a

from helpers import overlay, signal_helper
from helpers.signal_helper import generateSinSum, calculate_error
from helpers.csv_helper import read_in_transfer_function, read_in_signal, save_signale
from classes.transfer_function_class import transfer_function_class
from helpers.apply_transfer_function import apply_transfer_function
from classes.signal_class import signal_class


from blocks.generate_BBsignal import generate_BBsignal
from blocks.compute_Uquest_from_Uout import compute_Uquest_from_Uout
from blocks.compute_K_from_a import compute_K_from_a
from blocks.compute_Uin_from_Uquest import compute_Uin_from_Uquest
from blocks.compute_a_from_Uin_Uquet import compute_a_from_Uin_Uquet
from settings import project_path, mock_data_path
from settings import mock_system
from blocks import get_H
from helpers.signal_helper import find_nearest
from helpers.plot_helper import plot_K
import math
from copy import copy
import os

def create_mock_K(points, linearVpp_in_mV) :

    n = int(np.floor(points/2))

    K_pos = np.zeros([n,2])
    K_pos[:,0] = np.linspace(0, 300, n)

    ind = find_nearest(K_pos[:,0], linearVpp_in_mV/2)

    K_pos[:, 1][:ind+1] = K_pos[:,0][:ind+1]

    a = np.sin(np.linspace(0,math.pi/2, K_pos.shape[0]-ind))

    K_pos[:, 1][ind:] =a*K_pos[ind, 1]/math.pi*2 + K_pos[ind, 1]

    K_neg = -np.fliplr([K_pos])[0]

    K = np.concatenate((K_neg[:-1,:], K_pos), axis=0)

    return K


def flip_K(K):

    K_flipped = copy(K)
    K_flipped[:,0] = K[:,1]
    K_flipped[:, 1] = K[:, 0]

    return K_flipped


K = create_mock_K(10, 300)
K_flipped = flip_K(K)

plot_K(K_flipped)
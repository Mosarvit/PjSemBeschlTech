from unittest import TestCase
import unittest
from numpy import genfromtxt
from scipy import linalg
import matplotlib.pyplot as plt
from blocks.adjust_H import adjust_H
from blocks.adjust_a import adjust_a

from helpers import overlay, signal_helper
from helpers.signal_helper import generateSinSum
from helpers.csv_helper import read_in_transfer_function
from classes.transfer_function_class import transfer_function_class
from helpers.apply_transfer_function import apply_transfer_function


from blocks.generate_BBsignal import generate_BBsignal
from blocks.compute_Uquest_from_Uout import compute_Uquest_from_Uout
from blocks.compute_K_from_a import compute_K_from_a
from blocks.compute_Uin_from_Uquest import compute_Uin_from_Uquest
from blocks.compute_a_from_Uin_Uquest import compute_a_from_Uin_Uquest
from settings import project_path, mock_data_path
from settings import mock_system
from blocks import get_H
import os



import numpy as np


class test_set_sample_rate(TestCase):

    def __init__(self, *args, **kwargs):
        super(test_set_sample_rate, self).__init__(*args, **kwargs)

    def test_setSampleRate(self):

        Uin = genfromtxt(mock_data_path + 'Uin_jens.csv', delimiter=',')

        sampleRate = 1e9

        T = max(Uin[:, 0]) - min(Uin[:, 0])
        lenght_new = int(np.floor(T * sampleRate))

        Uin_computed = signal_helper.set_sample_rate(Uin, sampleRate);

        self.assertTrue(Uin_computed.shape[0] == lenght_new)
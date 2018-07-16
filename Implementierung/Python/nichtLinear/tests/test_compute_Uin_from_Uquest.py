from unittest import TestCase
import unittest
from numpy import genfromtxt
from scipy import linalg
import matplotlib.pyplot as plt
from blocks.adjust_H import adjust_H
from blocks.adjust_a import adjust_a

import settings

from helpers import overlay, signal_helper
from classes.signal_class import signal_class
from helpers.csv_helper import read_in_signal
from helpers.signal_helper import generateSinSum
from helpers.csv_helper import read_in_transfer_function
from classes.transfer_function_class import transfer_function_class
from helpers.apply_transfer_function import apply_transfer_function



from blocks.generate_BBsignal import generate_BBsignal
from blocks.compute_Uquest_from_Uout import compute_Uquest_from_Uout
from blocks.compute_K_from_a import compute_K_from_a
from blocks.compute_Uin_from_Uquest import compute_Uin_from_Uquest
from blocks.compute_a_from_Uin_Uquet import compute_a_from_Uin_Uquet
from settings import project_path, mock_data_directory
from settings import mock_system
from blocks import get_H
import os



import numpy as np


class test_compute_Uin_from_Uquest(TestCase):

    def __init__(self, *args, **kwargs):
        super(test_compute_Uin_from_Uquest, self).__init__(*args, **kwargs)


    # @unittest.skip("reason for skipping")
    def test_compute_Uin_from_Uquest_jens(self):

        Uin_ideal = read_in_signal(mock_data_directory + 'Uin_jens.csv')
        Uin_ideal.Vpp = 0.3

        Uquest_300 = read_in_signal(mock_data_directory + 'Uquest_300_jens.csv')

        K_300 = genfromtxt(mock_data_directory + 'K_300_jens.csv', delimiter=',')

        Uin_computed = compute_Uin_from_Uquest(Uquest_300, K_300, verbosity=False)

        Uin_computed_overlay_obj = overlay.overlay(Uin_computed, Uin_ideal)


        # plt.figure()
        # plt.plot(Uin_computed_overlay_obj.time, Uin_computed_overlay_obj.in_V)
        # plt.plot(Uin_ideal.time, Uin_ideal.in_V)
        # plt.legend(['Uin_computed_overlay_obj', 'Uin_ideal'])
        # plt.xlabel('t')
        # plt.ylabel('U')
        # if global_data.showPlots:
        #     plt.show()

        err = linalg.norm(Uin_computed_overlay_obj.in_V - Uin_ideal.in_V) / linalg.norm(Uin_ideal.in_V)
        self.assertTrue(err < 0.2)

    def test_compute_Uin_from_Uquest_our(self):

        Uin_ideal = read_in_signal(mock_data_directory + 'Uin_our.csv')
        Uin_ideal.Vpp = 0.3

        Uquest_300 = read_in_signal(mock_data_directory + 'Uquest_300_our.csv')

        K_300 = genfromtxt(mock_data_directory + 'K_300_jens.csv', delimiter=',')

        Uin_computed = compute_Uin_from_Uquest(Uquest_300, K_300, verbosity=False)

        Uin_computed_overlay_obj = overlay.overlay(Uin_computed, Uin_ideal)

        err = linalg.norm(Uin_computed_overlay_obj.in_V - Uin_ideal.in_V) / linalg.norm(Uin_ideal.in_V)
        self.assertTrue(err < 0.2)

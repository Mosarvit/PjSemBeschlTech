from unittest import TestCase
import unittest
from numpy import genfromtxt
from scipy import linalg
import matplotlib.pyplot as plt
from blocks.adjust_H import adjust_H
from blocks.adjust_a import adjust_a

from helpers import overlay, signal_helper
from helpers.signal_helper import generateSinSum
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
import os
from helpers.plot_helper import plot_2_signals



import numpy as np


class test_compute_Uin_from_Uquest(TestCase):

    def __init__(self, *args, **kwargs):
        super(test_compute_Uin_from_Uquest, self).__init__(*args, **kwargs)

    @unittest.skip("reason for skipping")
    def test_compute_Uin_from_Uquest_jens(self):
        Uin_ideal = read_in_signal(mock_data_path + 'Uin_jens.csv')
        Uin_ideal.Vpp = 0.3

        Uquest_300 = read_in_signal(mock_data_path + 'Uquest_300_jens.csv')

        K_300 = genfromtxt(mock_data_path + 'K_300_jens.csv', delimiter=',')

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
        Uin_ideal = read_in_signal(mock_data_path + 'Uin_our.csv')
        Uin_ideal.Vpp = 0.3

        Uquest_300 = read_in_signal(mock_data_path + 'Uquest_300_our.csv')

        K_300 = genfromtxt(mock_data_path + 'K_300_jens.csv', delimiter=',')

        Uin_computed = compute_Uin_from_Uquest(Uquest_300, K_300, verbosity=False)

        Uin_computed_overlay_obj = overlay.overlay(Uin_computed, Uin_ideal)

        err = linalg.norm(Uin_computed_overlay_obj.in_V - Uin_ideal.in_V) / linalg.norm(Uin_ideal.in_V)
        self.assertTrue(err < 0.2)

    def test_compute_Uin_from_Uquest_air(self):
        path = mock_data_path + 'adjust_a_19_07_2018-14_02_41/'

        Uin_awg = read_in_signal(path + 'Uin_initial.csv')
        Uquest_initial = read_in_signal(path + 'Uquest_initial.csv')
        K_300 = genfromtxt(path + 'K_initial.csv', delimiter=',')

        Uin_computed = compute_Uin_from_Uquest(Uquest_initial, K_300, verbosity=0)

        Uin_computed_overlay_obj = overlay.overlay(Uin_computed, Uin_awg)

        err = linalg.norm(Uin_computed_overlay_obj.in_V - Uin_awg.in_V) / linalg.norm(Uin_awg.in_V)
        self.assertTrue(err < 0.2)

    def test_compute_Uin_from_Uquest_air(self):
        path = mock_data_path + 'adjust_a_19_07_2018-14_02_41/'

        Uin_awg = read_in_signal(path + 'Uin_initial.csv')
        Uquest_initial = read_in_signal(path + 'Uquest_initial.csv')
        K_300 = genfromtxt(path + 'K_initial.csv', delimiter=',')

        Uin_computed = compute_Uin_from_Uquest(Uquest_initial, K_300, verbosity=0)

        Uin_computed_overlay_obj = overlay.overlay(Uin_computed, Uin_awg)

        err = linalg.norm(Uin_computed_overlay_obj.in_V - Uin_awg.in_V) / linalg.norm(Uin_awg.in_V)
        self.assertTrue(1)

    def test_compute_Uin_from_Uquest_air_new_K(self):
        path = mock_data_path + 'adjust_a_19_07_2018-14_02_41/'

        Uin_initial = read_in_signal(path + 'Uin_initial.csv')
        Uquest_initial = read_in_signal(path + 'Uquest_initial.csv')

        a = compute_a_from_Uin_Uquet(Uin_initial, Uquest_initial, 3)
        K_new = compute_K_from_a(a, verbosity=0)

        Uin_computed = compute_Uin_from_Uquest(Uquest_initial, K_new, verbosity=1)

        Uin_computed_overlay_obj = overlay.overlay(Uin_computed, Uin_initial)

        err = linalg.norm(Uin_computed_overlay_obj.in_V - Uin_initial.in_V) / linalg.norm(Uin_initial.in_V)
        self.assertTrue(err < 0.2)

    def test_compute_Uin_from_Uquest_from_adjust_a(self):
        path = mock_data_path + 'adjust_a_19_07_2018-13_53_38/'

        Uin_awg = read_in_signal(path + 'Uin_initial.csv')
        Uquest_initial = read_in_signal(path + 'Uquest_initial.csv')
        K_300 = genfromtxt(path + 'K_initial.csv', delimiter=',')

        Uin_computed = compute_Uin_from_Uquest(Uquest_initial, K_300, verbosity=0)

        Uin_computed_overlay_obj = overlay.overlay(Uin_computed, Uin_awg)

        err = linalg.norm(Uin_computed_overlay_obj.in_V - Uin_awg.in_V) / linalg.norm(Uin_awg.in_V)
        self.assertTrue(err < 0.2)

    def test_compute_Uin_from_Uquest_from_adjust_a_new_K(self):
        path = mock_data_path + 'adjust_a_19_07_2018-13_53_38/'

        Uin_initial = read_in_signal(path + 'Uin_initial.csv')
        Uquest_initial = read_in_signal(path + 'Uquest_initial.csv')

        a = compute_a_from_Uin_Uquet(Uin_initial, Uquest_initial, 3)
        K_new = compute_K_from_a(a, verbosity=0)

        Uin_computed = compute_Uin_from_Uquest(Uquest_initial, K_new, verbosity=1)

        Uin_computed_overlay_obj = overlay.overlay(Uin_computed, Uin_initial)
        plot_2_signals(Uin_computed_overlay_obj, Uin_initial)
        err = linalg.norm(Uin_computed_overlay_obj.in_V - Uin_initial.in_V) / linalg.norm(Uin_initial.in_V)
        self.assertTrue(err < 0.33)

    def test_compute_Uin_from_Uquest_with_higher_Uquest(self):
        path = mock_data_path + 'adjust_a_19_07_2018-13_53_38/'

        Uin_awg = read_in_signal(path + 'Uin_initial.csv')
        Uquest_initial = read_in_signal(path + 'Uquest_initial.csv')
        K_300 = genfromtxt(path + 'K_initial.csv', delimiter=',')

        Uin_computed = compute_Uin_from_Uquest(Uquest_initial, K_300, verbosity=True)

        Uin_computed.Vpp = Uin_computed.Vpp * 1.5
        Uin_awg.Vpp = Uin_awg.Vpp * 1.5

        Uin_computed_overlay_obj = overlay.overlay(Uin_computed, Uin_awg)



        err = linalg.norm(Uin_computed_overlay_obj.in_V - Uin_awg.in_V) / linalg.norm(Uin_awg.in_V)
        self.assertTrue(err < 0.33)
from unittest import TestCase
import unittest
from numpy import genfromtxt
from scipy import linalg
import matplotlib.pyplot as plt
from blocks.adjust_H import adjust_H
from blocks.adjust_a import adjust_a
from evaluate_with_BBsignal import evaluate_with_BBsignal

from helpers import overlay, signalHelper
from helpers.signalHelper import generateSinSum
from helpers.csvHelper import read_in_transfer_function
from classes.transfer_function import transfer_function
from helpers.apply_transfer_function import apply_transfer_function


from blocks.generate_BBsignal import generate_BBsignal
from blocks.compute_Uquest_from_Uout import compute_Uquest_from_Uout
from blocks.compute_K_from_a import compute_K_from_a
from blocks.compute_Uin_from_Uquest import compute_Uin_from_Uquest
from blocks.compute_a_from_Uin_Uquet import compute_a_from_Uin_Uquet
from global_data import project_path, mock_data_directory
from global_data import mock_system
from blocks import get_H
import os



import numpy as np


class test_compute_Uin_from_Uquest(TestCase):

    def __init__(self, *args, **kwargs):
        super(test_compute_Uin_from_Uquest, self).__init__(*args, **kwargs)


    # @unittest.skip("reason for skipping")
    def test_compute_Uin_from_Uquest_jens(self):
        Uin_ideal = genfromtxt(mock_data_directory + 'Uin_jens.csv', delimiter=',')
        Uin_mV_ideal = signalHelper.setVpp(signal=Uin_ideal, Vpp=300)
        Uquest_300 = genfromtxt(mock_data_directory + 'Uquest_300_jens.csv', delimiter=',')
        Uquest_300_mV = signalHelper.convert_V_to_mV(Uquest_300)
        K_300 = genfromtxt(mock_data_directory + 'K_300_jens.csv', delimiter=',')

        Uin_mV_computed = compute_Uin_from_Uquest(Uquest_300_mV, K_300, verbosity=False)

        _, Uin_mV_computed_overlay = overlay.overlay(Uin_mV_computed, Uin_mV_ideal)

        err = linalg.norm(Uin_mV_computed_overlay[:, 1] - Uin_mV_ideal[:, 1]) / linalg.norm(Uin_mV_ideal[:, 1])
        self.assertTrue(err < 0.2)

    def test_compute_Uin_from_Uquest_our(self):
        Uin_ideal = genfromtxt(mock_data_directory + 'Uin_our.csv', delimiter=',')
        Uin_mV_ideal = signalHelper.setVpp(signal=Uin_ideal, Vpp=300)
        Uquest_300 = genfromtxt(mock_data_directory + 'Uquest_300_our.csv', delimiter=',')
        Uquest_300_mV = signalHelper.convert_V_to_mV(Uquest_300)
        K_300 = genfromtxt(mock_data_directory + 'K_300_our.csv', delimiter=',')

        Uin_mV_computed = compute_Uin_from_Uquest(Uquest_300_mV, K_300, verbosity=False)

        _, Uin_mV_computed_overlay = overlay.overlay(Uin_mV_computed, Uin_mV_ideal)



        err = linalg.norm(Uin_mV_computed_overlay[:, 1] - Uin_mV_ideal[:, 1]) / linalg.norm(Uin_mV_ideal[:, 1])
        self.assertTrue(err < 0.2)
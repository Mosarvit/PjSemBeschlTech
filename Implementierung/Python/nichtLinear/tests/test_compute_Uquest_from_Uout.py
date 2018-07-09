from unittest import TestCase
import unittest
from numpy import genfromtxt
from scipy import linalg
import matplotlib.pyplot as plt
from blocks.adjust_H import adjust_H
from blocks.adjust_a import adjust_a
from evaluate_with_BBsignal import evaluate_with_BBsignal

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
from global_data import project_path, mock_data_directory
from global_data import mock_system
from blocks import get_H
import os



import numpy as np


class test_compute_Uquest_from_Uout(TestCase):

    def __init__(self, *args, **kwargs):
        super(test_compute_Uquest_from_Uout, self).__init__(*args, **kwargs)

    def test_compute_Uquest_from_Uout_300_jens(self):

       Uout_300 = read_in_signal(mock_data_directory + 'Uout_300_jens.csv')
       Uquest_300_ideal = read_in_signal(mock_data_directory + 'Uquest_300_jens.csv')

       H = read_in_transfer_function( mock_data_directory + 'H_jens.csv' )

       Uquest_300_computed = compute_Uquest_from_Uout(Uout=Uout_300, H=H, verbosity=False)

       err = linalg.norm(Uquest_300_computed.in_V - Uquest_300_ideal.in_V) / linalg.norm( Uquest_300_ideal.in_V)
       self.assertTrue(err < 0.03)

    def test_compute_Uquest_from_Uout_300_our(self):
        Uout_300 = read_in_signal(mock_data_directory + 'Uout_300_our.csv')
        Uquest_300_ideal = read_in_signal(mock_data_directory + 'Uquest_300_our.csv')

        H = read_in_transfer_function(mock_data_directory + 'H_our.csv')

        Uquest_300_computed = compute_Uquest_from_Uout(Uout=Uout_300, H=H, verbosity=False)

        err = linalg.norm(Uquest_300_computed.in_V - Uquest_300_ideal.in_V) / linalg.norm(Uquest_300_ideal.in_V)
        self.assertTrue(err < 0.03)

    def test_compute_Uquest_from_Uout_with_BBsignal_ideal(self):

        BBsignal_ideal = read_in_signal(mock_data_directory + 'BBsignal_our.csv')
        Uquest_from_BBsignal_ideal = read_in_signal(mock_data_directory + 'Uquest_from_BBsignal_our.csv')

        H = read_in_transfer_function(mock_data_directory + 'H_our.csv')

        Uquest_from_BBsignal_computed = compute_Uquest_from_Uout(Uout=BBsignal_ideal, H=H, verbosity=False)

        err = linalg.norm(Uquest_from_BBsignal_computed.in_V - Uquest_from_BBsignal_ideal.in_V) / linalg.norm(Uquest_from_BBsignal_ideal.in_V)
        self.assertTrue(err<0.04)



    # @unittest.skip("reason for skipping")
    def test_compute_Uquest_from_Uout_catch_imaginary(self):

        BBsignal_ideal = read_in_signal(mock_data_directory + 'BBsignal_our.csv')

        H = read_in_transfer_function(mock_data_directory + 'H_our.csv')

        Uquest_from_BBsignal_computed = compute_Uquest_from_Uout(Uout=BBsignal_ideal, H=H, verbosity=False)

        self.assertFalse(np.iscomplex(Uquest_from_BBsignal_computed.in_V.any()))
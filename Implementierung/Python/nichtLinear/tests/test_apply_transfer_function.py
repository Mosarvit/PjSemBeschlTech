from unittest import TestCase
import unittest
from numpy import genfromtxt
from scipy import linalg
import matplotlib.pyplot as plt
from blocks.adjust_H import adjust_H
from blocks.adjust_a import adjust_a

from helpers import overlay, signal_helper
from helpers.signal_helper import generateSinSum
from helpers.csv_helper import read_in_transfer_function, read_in_signal, read_in_transfer_function_old_convention
from classes.transfer_function_class import transfer_function_class
from helpers.apply_transfer_function import apply_transfer_function
from classes.signal_class import signal_class


from blocks.generate_BBsignal import generate_BBsignal
from blocks.compute_Uquest_from_Uout import compute_Uquest_from_Uout
from blocks.compute_K_from_a import compute_K_from_a
from blocks.compute_Uin_from_Uquest import compute_Uin_from_Uquest
from blocks.compute_a_from_Uin_Uquet import compute_a_from_Uin_Uquet
from global_data import project_path, mock_data_directory
from helpers.plot_helper import plot_transfer_function
from global_data import mock_system
from blocks import get_H
import os



import numpy as np


class test_apply_transfer_function(TestCase):

    def __init__(self, *args, **kwargs):
        super(test_apply_transfer_function, self).__init__(*args, **kwargs)


    def test_apply_transfer_function_BBsignal(self):

        H = read_in_transfer_function(mock_data_directory + 'H_jens.csv')

        Uout_300_ideal = generate_BBsignal()
        Uquest_300 = apply_transfer_function(Uout_300_ideal, H.get_inverse())
        Uout_computed = apply_transfer_function(Uquest_300, H)

        err = linalg.norm(Uout_computed.in_V - Uout_300_ideal.in_V) / linalg.norm(Uout_300_ideal.in_V)

        self.assertTrue(err < 0.03)


    def test_apply_transfer_function(self):

        H = read_in_transfer_function(mock_data_directory + 'H_jens.csv')

        Uout_300_ideal = read_in_signal(mock_data_directory + 'Uout_300_jens.csv')
        # Uout_300_ideal = Uout_300_ideal.get_signal_in_V_old_convention()
        Uquest_300 = apply_transfer_function(Uout_300_ideal, H.get_inverse())
        Uout_computed = apply_transfer_function(Uquest_300, H)

        err = linalg.norm(Uout_computed.in_V - Uout_300_ideal.in_V) / linalg.norm(Uout_300_ideal.in_V)

        self.assertTrue(err < 0.04)

    def test_apply_transfer_function_2(self):

        H = read_in_transfer_function_old_convention(mock_data_directory + 'adjustH/Messung3/Ha_0.csv',
                                      mock_data_directory + 'adjustH/Messung3/Hp_0.csv')

        Uout_300_ideal = read_in_signal(mock_data_directory + 'Uout_300_jens.csv')
        # Uout_300_ideal = Uout_300_ideal.get_signal_in_V_old_convention()
        Uquest_300 = apply_transfer_function(Uout_300_ideal, H.get_inverse())
        Uout_computed = apply_transfer_function(Uquest_300, H)

        err = linalg.norm(Uout_computed.in_V - Uout_300_ideal.in_V) / linalg.norm(Uout_300_ideal.in_V)

        self.assertTrue(err < 0.04)
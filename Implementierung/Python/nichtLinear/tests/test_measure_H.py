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
from blocks.compute_a_from_Uin_Uquet import compute_a_from_Uin_Uquet
from settings import project_path, mock_data_path
from settings import mock_system
from blocks.determine_H import determine_H
from classes.transfer_function_class import transfer_function_class
from helpers.csv_helper import read_in_transfer_function_old_convention, read_in_signal, read_in_transfer_function_complex
from helpers.plot_helper import plot_2_transfer_functions, plot_2_signals, plot_transfer_function
from settings import project_path, last_directory_used
import os
import settings



import numpy as np


class test_measure_H(TestCase):

    def __init__(self, *args, **kwargs):
        super(test_measure_H, self).__init__(*args, **kwargs)

    def test_measure_H(self):

        H_ideal = mock_system.H
        H_computed = determine_H()

        err = linalg.norm(H_computed.c - H_ideal.c) / linalg.norm(H_ideal.c)

        verbosity = 0
        if verbosity :
            plot_2_transfer_functions(H1=H_ideal, H2=H_computed, legend1='H_ideal', legend2='H_computed')

        self.assertTrue(err<0.04)
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
from global_data import project_path, mock_data_directory
from global_data import mock_system
from blocks import get_H
import os



import numpy as np


class test_compute_K_from_a(TestCase):

    def __init__(self, *args, **kwargs):
        super(test_compute_K_from_a, self).__init__(*args, **kwargs)


    def test_compute_K_from_a_jens(self):
        K_300_ideal = genfromtxt(mock_data_directory + 'K_300_jens.csv', delimiter=',')

        a_300 = genfromtxt(mock_data_directory + 'a_300_jens.csv', delimiter=',')

        K_computed = compute_K_from_a(a_300, verbosity=False)

        err = linalg.norm(K_computed - K_300_ideal) / linalg.norm(K_300_ideal)
        self.assertTrue(err < 1e-3)

    def test_compute_K_from_a_our(self):
        K_300_ideal = genfromtxt(mock_data_directory + 'K_300_our.csv', delimiter=',')

        a_300 = genfromtxt(mock_data_directory + 'a_300_our.csv', delimiter=',')

        K_computed = compute_K_from_a(a_300, verbosity=False)

        err = linalg.norm(K_computed - K_300_ideal) / linalg.norm(K_300_ideal)
        self.assertTrue(err < 1e-3)
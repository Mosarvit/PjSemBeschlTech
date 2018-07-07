from unittest import TestCase
import unittest
from numpy import genfromtxt
from scipy import linalg
import matplotlib.pyplot as plt
from blocks.adjust_H import adjust_H
from blocks.adjust_a import adjust_a
from evaluate_with_BBsignal import evaluate_with_BBsignal

from helpers import overlay, signalHelper
from helpers.csvHelper import read_in_signal
from helpers.signalHelper import generateSinSum
from helpers.csvHelper import read_in_transfer_function
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


class test_compute_a_from_Uin_Uquest(TestCase):

    def __init__(self, *args, **kwargs):
        super(test_compute_a_from_Uin_Uquest, self).__init__(*args, **kwargs)

    # @unittest.skip("reason for skipping")
    def test_compute_a_from_Uin_Uquest_300_jens(self):
        Uquest_300 = read_in_signal(mock_data_directory + 'Uquest_300_jens.csv')
        Uin = read_in_signal(mock_data_directory + 'Uin_jens.csv')
        Uin.Vpp = 0.3

        a_300_ideal = genfromtxt(mock_data_directory + 'a_300_jens.csv', delimiter=',')

        a_300_computed = compute_a_from_Uin_Uquet(Uin=Uin, Uquest=Uquest_300, N=3)

        err = linalg.norm(a_300_computed - a_300_ideal) / linalg.norm(a_300_ideal)
        self.assertTrue(err < 1e-3)

    def test_compute_a_from_Uin_Uquest_300_our(self):
        Uquest_300 = read_in_signal(mock_data_directory + 'Uquest_300_our.csv')
        Uin = read_in_signal(mock_data_directory + 'Uin_our.csv')
        Uin.Vpp = 0.3

        a_300_ideal = genfromtxt(mock_data_directory + 'a_300_our.csv', delimiter=',')

        a_300_computed = compute_a_from_Uin_Uquet(Uin=Uin, Uquest=Uquest_300, N=3)

        err = linalg.norm(a_300_computed - a_300_ideal) / linalg.norm(a_300_ideal)
        self.assertTrue(err < 1e-3)
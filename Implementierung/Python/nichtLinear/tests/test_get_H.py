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


class test_get_H(TestCase):

    def __init__(self, *args, **kwargs):
        super(test_get_H, self).__init__(*args, **kwargs)

    @unittest.skip("currently not working")
    def test_get_H(self):

        fmax = 80e6
        vpp = 40e-3
        bits = 9
        f, Ha, Hph = get_H.compute(fmax, vpp, bits=bits, use_mock_system=1, showPlots=0)

        plt.figure()
        plt.plot(f, Ha)
        plt.title('Amplitude')
        plt.xlabel('f')

        if 1:
            plt.show()

        plt.figure()
        plt.plot(f, Hph)
        plt.title('Phase in rad')
        plt.xlabel('f')

        if 1:
            plt.show()

        self.assertTrue(1)
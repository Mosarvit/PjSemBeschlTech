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


class test_adjust_a(TestCase):

    def __init__(self, *args, **kwargs):
        super(test_adjust_a, self).__init__(*args, **kwargs)

    @unittest.skip("currently not working")
    def test_adjust_a(self):
        # erster Logik Test
        x = np.linspace(0,10)
        a_old = [0, 1, 0]

        u_ideal1 = np.zeros((len(x), 2))
        u_ideal2 = np.zeros((len(x), 2))
        u_ideal1[:, 0] = x
        u_ideal2[:, 0] = x
        u_ideal1[:, 1] = [np.power(xi, 2) for xi in x]
        u_ideal2[:, 1] = u_ideal1[:,1] + [2*np.power(xi, 3) for xi in x]
        a_new = adjust_a(a_old, x, u_ideal1, u_ideal2, 1)
        print(a_new)


        err = linalg.norm(0)

        self.assertTrue(err < 0.001) # we allow an error of 0.1% for the start, but it should be better
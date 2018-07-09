from unittest import TestCase
import unittest
from numpy import genfromtxt
from scipy import linalg
import matplotlib.pyplot as plt
from blocks.adjust_H import adjust_H
from blocks.adjust_a import adjust_a
from evaluate_with_BBsignal import evaluate_with_BBsignal
from evaluate_with_BBsignal_adjust_H import evaluate_with_BBsignal_adjust_H
from helpers.plot_helper import plot_two_signals


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
from global_data import mock_system, show_plots
from blocks import get_H
import os



import numpy as np


class test_evaluate_with_BBsignal(TestCase):

    def __init__(self, *args, **kwargs):
        super(test_evaluate_with_BBsignal, self).__init__(*args, **kwargs)

    def test_evaluate_with_BBsignal_low_amplitude(self):

        Uout_ideal, Uout_measured = evaluate_with_BBsignal_adjust_H(num_iters=1)

        # diff = linalg.norm(Uout_measured.in_V - Uout_ideal.in_V)
        # nrm = linalg.norm(Uout_ideal.in_V)

        err = linalg.norm(Uout_measured.in_V - Uout_ideal.in_V) / linalg.norm(Uout_ideal.in_V)

        plot_two_signals(Uout_ideal, Uout_measured, 'Uout_measured', 'Uout_ideal')

        self.assertTrue(err < 0.15)



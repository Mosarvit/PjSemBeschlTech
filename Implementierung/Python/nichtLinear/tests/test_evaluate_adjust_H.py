from unittest import TestCase
import unittest
from numpy import genfromtxt
from scipy import linalg
import matplotlib.pyplot as plt
from blocks.adjust_H import adjust_H
from blocks.adjust_a import adjust_a
from evaluate_adjust_H import evaluate_adjust_H
from helpers.plot_helper import plot_2_signals, plot_2_transfer_functions


from helpers.overlay import overlay
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
from settings import mock_system, show_plots
from blocks import get_H
import os



import numpy as np


class test_evaluate_adjust_H(TestCase):


    def __init__(self, *args, **kwargs):
        super(test_evaluate_adjust_H, self).__init__(*args, **kwargs)

    # @unittest.skip("currently not relevant")
    def test_evaluate_adjust_H_0_steps(self):

        Uout_ideal, Uout_measured, _, _ = evaluate_adjust_H(num_iters=1, verbosity=0)

        Uout_measured = overlay(Uout_measured, Uout_ideal)

        err = linalg.norm(Uout_measured.in_V - Uout_ideal.in_V) / linalg.norm(Uout_ideal.in_V)

        verbosity = 0
        if verbosity :
            plot_2_signals(Uout_ideal, Uout_measured, 'Uout_measured', 'Uout_ideal')

        self.assertTrue(err < 0.07)


    def test_evaluate_adjust_H_1_step(self):

        Uout_ideal, Uout_measured, H_0, H_last = evaluate_adjust_H(num_iters=5, verbosity=0)

        err = linalg.norm(H_0.a - H_last.a) / linalg.norm(H_last.a)

        verbosity = 0

        if verbosity :
            plot_2_transfer_functions(H_0, H_last, 'H_0', 'H_last')

        self.assertTrue(err < 0.02)



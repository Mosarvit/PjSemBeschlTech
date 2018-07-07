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


class test_adjust_H(TestCase):

    def __init__(self, *args, **kwargs):
        super(test_adjust_H, self).__init__(*args, **kwargs)

    def test_adjust_H_a_trivial(self):

        Halt = read_in_transfer_function(mock_data_directory + 'H_jens.csv')

        Hneu_ideal = Halt

        t = np.linspace(0, .0001, 1000)
        Uout_ideal = generateSinSum(np.array([[1, 4], [2, 6], [3, 10]], np.int32), t)
        Uout_measured = Uout_ideal

        sigma_H = 0.5

        Hneu = adjust_H(Halt, Uout_ideal, Uout_measured, sigma_H)

        err = linalg.norm(Hneu.a - Hneu_ideal.a) / linalg.norm(Hneu_ideal.a)
        self.assertTrue(err < 0.001)

    def test_adjust_H_p_trivial(self):

        """
        trivial test:
        if
          Uout_measured = Uout_ideal
        than
          Hneu = Halt
        """

        Halt = read_in_transfer_function(mock_data_directory + 'H_jens.csv')
        Hneu_ideal = Halt

        t = np.linspace(0, 1e-5, 1000)
        Uout_ideal = generateSinSum(np.array([[1, 4], [2, 6], [3, 10]], np.int32), t)
        Uout_measured = Uout_ideal

        sigma_H = 0.5

        Hneu = adjust_H(Halt, Uout_ideal, Uout_measured, sigma_H)

        err = linalg.norm(Hneu.c - Hneu_ideal.c) / linalg.norm(Hneu_ideal.c)
        self.assertTrue(err < 0.001)

    def test_adjust_H(self):

        """
        if
          Uout_ideal is a sum of three sin functions
          Uout_measured = 2 * Uout_ideal
          sigma_H = 0.5,
        than
          Hneu.a = Halt.a * 1.5
        """

        Halt = read_in_transfer_function(mock_data_directory + 'H_jens.csv')
        Hneu_ideal = transfer_function_class(Halt.f)

        sigma_H = 0.5
        factor = 2
        Hneu_ideal.a = Halt.a * ( 1 + ( ( factor - 1 ) * sigma_H ) )
        Hneu_ideal.p = Halt.p

        t = np.linspace(0, 1e-5, 1000)
        # Do not change Signal because for about used formular signal has to contain every frequency possible
        Uout_ideal = generateSinSum(np.array([[1, 4 ],  [2, 6 ],  [3, 10 ]]), t)
        Uout_measured = np.zeros((Uout_ideal.shape[0], 2))
        Uout_measured[:, 0] = Uout_ideal[:, 0]
        Uout_measured[:,1] = [x*factor for x in Uout_ideal[:, 1]]

        Hneu = adjust_H(Halt, Uout_ideal, Uout_measured, sigma_H)

        err = linalg.norm(Hneu.c - Hneu_ideal.c) / linalg.norm(Hneu_ideal.c)

        self.assertTrue(err < 0.001) # we allow an error of 0.1% for the start, but it should be better
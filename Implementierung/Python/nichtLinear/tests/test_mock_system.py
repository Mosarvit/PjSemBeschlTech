from unittest import TestCase
import unittest
from numpy import genfromtxt
from scipy import linalg
import matplotlib.pyplot as plt
from blocks.adjust_H import adjust_H
from blocks.adjust_a import adjust_a

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
from settings import project_path, mock_data_directory
from settings import mock_system
from helpers.csv_helper import read_in_signal
from blocks import get_H
import os



import numpy as np


class test_mock_system(TestCase):

    def __init__(self, *args, **kwargs):
        if __name__ == '__main__':
            unittest.main(exit=False)
        super(test_mock_system, self).__init__(*args, **kwargs)

    def test_mock_system(self):

        sample_rate_DSO = 9999e5

        Uout_ideal = read_in_signal(mock_data_directory + 'Uout_300_our.csv')
        Uquest_ideal = read_in_signal(mock_data_directory + 'Uquest_300_our.csv')

        mock_system.H = read_in_transfer_function(mock_data_directory + 'H_our.csv')

        mock_system.write_to_AWG(Uin=Uquest_ideal)
        _, Uout_computed = mock_system.read_from_DSO(sample_rate_DSO=sample_rate_DSO)

        Uout_computed = overlay(Uout_computed, Uout_ideal)

        err = linalg.norm(Uout_computed.in_V - Uout_ideal.in_V) / linalg.norm(Uout_ideal.in_V)

        self.assertTrue(err < 0.04)

    if __name__=='__main__':
        try:
            unittest.main()
        except SystemExit as inst:
            if inst.args[0] is True: # raised by sys.exit(True) when tests failed
                raise
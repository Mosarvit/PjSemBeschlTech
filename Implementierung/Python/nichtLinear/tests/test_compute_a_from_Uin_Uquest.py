import unittest
from unittest import TestCase

from numpy import genfromtxt
from scipy import linalg

from blocks.compute_a_from_Uin_Uquet import compute_a_from_Uin_Uquet
from helpers.csv_helper import read_in_signal
from helpers.tezt_helper import  finilize_tezt
from settings import mock_data_path


class test_compute_a_from_Uin_Uquest(TestCase):

    def __init__(self, *args, **kwargs):
        super(test_compute_a_from_Uin_Uquest, self).__init__(*args, **kwargs)

    # @unittest.skip("The mock data cannot be correct, since the timeperiod of Uquest_300_jens.csv and Uin_jens.csv are too different")
    # def test_compute_a_from_Uin_Uquest_300_jens(self):
    #     Uquest_300 = read_in_signal(mock_data_path + 'Uquest_300_jens.csv')
    #     Uin = read_in_signal(mock_data_path + 'Uin_jens.csv')
    #     Uin.Vpp = 0.3
    #
    #     a_300_ideal = genfromtxt(mock_data_path + 'a_300_jens.csv', delimiter=',')
    #
    #     a_300_computed = compute_a_from_Uin_Uquet(Uin=Uin, Uquest=Uquest_300, N=3)
    #
    #     test_succeeded = finilize_test_with_signal(U_computed=a_300_computed, set_ideal_signal=0, verbosity=0)
    #     self.assertTrue(test_succeeded)

    def test_compute_a_from_Uin_Uquest_300_our(self):
        Uquest_300 = read_in_signal(mock_data_path + 'Uquest_300_our.csv')
        Uin = read_in_signal(mock_data_path + 'Uin_our.csv')
        Uin.Vpp = 0.3

        a_300_ideal = genfromtxt(mock_data_path + 'a_300_our.csv', delimiter=',')

        a_300_computed = compute_a_from_Uin_Uquet(Uin=Uin, Uquest=Uquest_300, N=3)

        test_succeeded = finilize_tezt(values_computed=a_300_computed, set_ideal_values=0, verbosity=0)
        self.assertTrue(test_succeeded)
from unittest import TestCase

from numpy import genfromtxt
from scipy import linalg

from blocks.compute_K_from_a import compute_K_from_a
from helpers.tezt_helper import finilize_tezt_with
from settings import mock_data_path


class test_compute_K_from_a(TestCase):

    def __init__(self, *args, **kwargs):
        super(test_compute_K_from_a, self).__init__(*args, **kwargs)


    def test_compute_K_from_a_jens(self):
        K_300_ideal = genfromtxt(mock_data_path + 'K_300_jens.csv', delimiter=',')

        a_300 = genfromtxt(mock_data_path + 'a_300_jens.csv', delimiter=',')

        K_computed = compute_K_from_a(a_300, verbosity=False)

        test_succeeded = finilize_tezt_with(values_computed=K_computed, set_ideal_signal=0, verbosity=0)
        self.assertTrue(test_succeeded)

    def test_compute_K_from_a_our(self):
        K_300_ideal = genfromtxt(mock_data_path + 'K_300_our.csv', delimiter=',')

        a_300 = genfromtxt(mock_data_path + 'a_300_our.csv', delimiter=',')

        K_computed = compute_K_from_a(a_300, verbosity=False)

        test_succeeded = finilize_tezt_with(values_computed=K_computed, set_ideal_signal=0, verbosity=0)
        self.assertTrue(test_succeeded)
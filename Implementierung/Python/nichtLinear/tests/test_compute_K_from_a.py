from unittest import TestCase

from numpy import genfromtxt

from blocks.compute_K_from_a import compute_K_from_a
from helpers.csv_helper import read_in_signal
from helpers.plot_helper import plot_K, plot_2_Ks
from helpers.tezt_helper import finilize_tezt
from settings import mock_data_path
from blocks.compute_a_from_Uin_Uquet import compute_a_from_Uin_Uquet


class test_compute_K_from_a(TestCase):

    def __init__(self, *args, **kwargs):
        super(test_compute_K_from_a, self).__init__(*args, **kwargs)


    def test_compute_K_from_a_jens(self):
        K_300_ideal = genfromtxt(mock_data_path + 'K_300_jens.csv', delimiter=',')

        a_300 = genfromtxt(mock_data_path + 'a_300_jens.csv', delimiter=',')

        K_computed = compute_K_from_a(a_300, verbosity=False)

        test_succeeded = finilize_tezt(values_computed=K_computed, set_ideal_values=0, verbosity=0)
        self.assertTrue(test_succeeded)

    def test_compute_K_from_a_our(self):
        K_300_ideal = genfromtxt(mock_data_path + 'K_300_our.csv', delimiter=',')

        a_300 = genfromtxt(mock_data_path + 'a_300_our.csv', delimiter=',')

        K_computed = compute_K_from_a(a_300, verbosity=0)

        # plot_2_Ks(K_300_ideal, K_computed)

        test_succeeded = finilize_tezt(values_computed=K_computed, set_ideal_values=0, verbosity=0)
        self.assertTrue(test_succeeded)

    def test_compute_aK(self):
        Uquest_300 = read_in_signal(mock_data_path + 'Uquest_300_our.csv')
        Uin = read_in_signal(mock_data_path + 'Uin_our.csv')
        Uin.Vpp = 0.3

        a_300_ideal = genfromtxt(mock_data_path + 'a_300_our.csv', delimiter=',')

        a_300_computed = compute_a_from_Uin_Uquet(Uin=Uin, Uquest=Uquest_300, N=3)

        K_computed = compute_K_from_a(a_300_computed, verbosity=0)

        # plot_2_Ks(K_computed, K_computed)

        test_succeeded = finilize_tezt(values_computed=a_300_computed, set_ideal_values=0, verbosity=0)
        self.assertTrue(test_succeeded)

    def test_compute_aK1(self):
        Uquest_300 = read_in_signal(mock_data_path + 'Uquest_300_our.csv')
        Uin = read_in_signal(mock_data_path + 'Uin_our.csv')
        # Uin = Uquest_300
        Uin.Vpp = 0.3

        # K_300_ideal = genfromtxt(mock_data_path + 'K_300_our.csv', delimiter=',')

        a_300_computed = compute_a_from_Uin_Uquet(Uin=Uin, Uquest=Uquest_300, N=3)
        K_computed = compute_K_from_a(a_300_computed, verbosity=0)

        test_succeeded, K_ideal = finilize_tezt(values_computed=K_computed, set_ideal_values=0, verbosity=0)

        # plot_2_Ks(K_computed, K_300_ideal)

        self.assertTrue(test_succeeded)
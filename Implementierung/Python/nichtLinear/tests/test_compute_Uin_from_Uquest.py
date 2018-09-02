import unittest
from unittest import TestCase

from numpy import genfromtxt
from scipy import linalg

from blocks.compute_K_from_a import compute_K_from_a
from blocks.compute_Uin_from_Uquest import compute_Uin_from_Uquest
from blocks.compute_a_from_Uin_Uquest import compute_a_from_Uin_Uquest
from helpers import overlay
from helpers.csv_helper import read_in_signal
from helpers.overlay import overlay
from helpers.tezt_helper import finilize_tezt
from settings import mock_data_path


class test_compute_Uin_from_Uquest(TestCase):

    def __init__(self, *args, **kwargs):
        super(test_compute_Uin_from_Uquest, self).__init__(*args, **kwargs)

    # @unittest.skip("reason for skipping")
    # def test_compute_Uin_from_Uquest_jens(self):
    #     Uin_ideal = read_in_signal(mock_data_path + 'Uin_jens.csv')
    #     Uin_ideal.Vpp = 0.3
    #
    #     Uquest_300 = read_in_signal(mock_data_path + 'Uquest_300_jens.csv')
    #
    #     K_300 = genfromtxt(mock_data_path + 'K_300_jens.csv', delimiter=',')
    #
    #     Uin_computed = compute_Uin_from_Uquest(Uquest_300, K_300, verbosity=False)
    #
    #     Uin_computed_overlay_obj = overlay(Uin_computed, Uin_ideal)
    #
    #     test_succeeded = finilize_test_with_signal(U_computed=Uin_computed, set_ideal_signal=0, verbosity=0)
    #     self.assertTrue(test_succeeded)
    # @unittest.skip("Old Konvention for K")
    def test_compute_Uin_from_Uquest_our(self):
        Uin_ideal = read_in_signal(mock_data_path + 'Uin_our.csv')
        Uin_ideal.Vpp = 0.3

        Uquest_300 = read_in_signal(mock_data_path + 'Uquest_300_our.csv')

        a = compute_a_from_Uin_Uquest(Uin_ideal, Uquest_300, 3)
        K_new = compute_K_from_a(a, verbosity=0)

        Uin_computed, Uquest_addapted = compute_Uin_from_Uquest(Uquest_300, K_new, verbosity=0)

        Uin_computed_overlay_obj = overlay(Uin_computed, Uin_ideal)

        test_succeeded = finilize_tezt(values_computed=Uin_computed, set_accepted_values=0, verbosity=0)
        self.assertTrue(test_succeeded)

    def test_compute_Uin_from_Uquest_our_new_K(self):
        Uin_ideal = read_in_signal(mock_data_path + 'Uin_our.csv')
        Uin_ideal.Vpp = 0.3

        Uquest_300 = read_in_signal(mock_data_path + 'Uquest_300_our.csv')

        a = compute_a_from_Uin_Uquest(Uin_ideal, Uquest_300, 3)
        K_new = compute_K_from_a(a, verbosity=0)

        Uin_computed, Uquest_addapted = compute_Uin_from_Uquest(Uquest_300, K_new, verbosity=False)

        Uin_computed_overlay_obj = overlay(Uin_computed, Uin_ideal)

        test_succeeded = finilize_tezt(values_computed=Uin_computed, set_accepted_values=0, verbosity=0)
        self.assertTrue(test_succeeded)


    def test_compute_Uin_from_Uquest_air(self):
        path = mock_data_path + 'adjust_a_19_07_2018-14_02_41/'

        Uin_awg = read_in_signal(path + 'Uin_initial.csv')
        Uquest_initial = read_in_signal(path + 'Uquest_initial.csv')

        a = compute_a_from_Uin_Uquest(Uin_awg, Uquest_initial, 3)
        K_new = compute_K_from_a(a, verbosity=0)

        Uin_computed, Uquest_addapted = compute_Uin_from_Uquest(Uquest_initial, K_new, verbosity=0)

        Uin_computed_overlay_obj = overlay(Uin_computed, Uin_awg)

        test_succeeded = finilize_tezt(values_computed=Uin_computed, set_accepted_values=0, verbosity=0)
        self.assertTrue(test_succeeded)


    def test_compute_Uin_from_Uquest_air(self):
        path = mock_data_path + 'adjust_a_19_07_2018-14_02_41/'

        Uin_awg = read_in_signal(path + 'Uin_initial.csv')
        Uquest_initial = read_in_signal(path + 'Uquest_initial.csv')

        a = compute_a_from_Uin_Uquest(Uin_awg, Uquest_initial, 3)
        K_new = compute_K_from_a(a, verbosity=0)

        Uin_computed, Uquest_addapted = compute_Uin_from_Uquest(Uquest_initial, K_new, verbosity=0)


        Uin_computed_overlay_obj = overlay(Uin_computed, Uin_awg)

        test_succeeded = finilize_tezt(values_computed=Uin_computed, set_accepted_values=0, verbosity=0)
        self.assertTrue(test_succeeded)

    def test_compute_Uin_from_Uquest_air_new_K(self):
        path = mock_data_path + 'adjust_a_19_07_2018-14_02_41/'

        Uin_initial = read_in_signal(path + 'Uin_initial.csv')
        Uquest_initial = read_in_signal(path + 'Uquest_initial.csv')

        a = compute_a_from_Uin_Uquest(Uin_initial, Uquest_initial, 3)
        K_new = compute_K_from_a(a, verbosity=0)

        Uin_computed, Uquest_addapted = compute_Uin_from_Uquest(Uquest_initial, K_new, verbosity=0)

        Uin_computed_overlay_obj = overlay(Uin_computed, Uin_initial)

        test_succeeded = finilize_tezt(values_computed=Uin_computed, set_accepted_values=0, verbosity=0)
        self.assertTrue(test_succeeded)


    def test_compute_Uin_from_Uquest_from_adjust_a(self):
        path = mock_data_path + 'adjust_a_19_07_2018-13_53_38/'

        Uin_awg = read_in_signal(path + 'Uin_initial.csv')
        Uquest_initial = read_in_signal(path + 'Uquest_initial.csv')

        a = compute_a_from_Uin_Uquest(Uin_awg, Uquest_initial, 3)
        K_new = compute_K_from_a(a, verbosity=0)

        Uin_computed, Uquest_addapted = compute_Uin_from_Uquest(Uquest_initial, K_new, verbosity=0)

        Uin_computed_overlay_obj = overlay(Uin_computed, Uin_awg)

        test_succeeded = finilize_tezt(values_computed=Uin_computed, set_accepted_values=0, verbosity=0)
        self.assertTrue(test_succeeded)



    def test_compute_Uin_from_Uquest_from_adjust_a_new_K(self):
        path = mock_data_path + 'adjust_a_19_07_2018-13_53_38/'

        Uin_ideal = read_in_signal(path + 'Uin_initial.csv')
        Uquest_measured = read_in_signal(path + 'Uquest_initial.csv')

        a = compute_a_from_Uin_Uquest(Uin_ideal, Uquest_measured, 3)
        K_new = compute_K_from_a(a, verbosity=0)

        Uin_computed, Uquest_addapted = compute_Uin_from_Uquest(Uquest_measured, K_new, verbosity=0)

        Uin_computed_overlay_obj = overlay(Uin_computed, Uin_ideal)
        # plot_2_signals(Uin_computed_overlay_obj, Uin_initial)
        test_succeeded = finilize_tezt(values_computed=Uin_computed, set_accepted_values=0, verbosity=0)
        self.assertTrue(test_succeeded)


    def test_compute_Uin_from_Uquest_with_higher_Uquest(self):
        path = mock_data_path + 'adjust_a_19_07_2018-13_53_38/'

        Uin_awg = read_in_signal(path + 'Uin_initial.csv')
        Uquest_initial = read_in_signal(path + 'Uquest_initial.csv')
        
        a = compute_a_from_Uin_Uquest(Uin_awg, Uquest_initial, 3)
        K_new = compute_K_from_a(a, verbosity=0)

        Uin_computed, Uquest_addapted = compute_Uin_from_Uquest(Uquest_initial, K_new, verbosity=0)

        Uin_computed.Vpp = Uin_computed.Vpp * 1.5
        Uin_awg.Vpp = Uin_awg.Vpp * 1.5

        Uin_computed_overlay_obj = overlay(Uin_computed, Uin_awg)

        test_succeeded = finilize_tezt(values_computed=Uin_computed, set_accepted_values=0, verbosity=0)
        self.assertTrue(test_succeeded)

    def test_compute_Uin_from_Uquest_with_higher_Uquest_new_K(self):
        path = mock_data_path + 'adjust_a_19_07_2018-13_53_38/'

        Uin_ideal = read_in_signal(path + 'Uin_initial.csv')
        Uquest_initial = read_in_signal(path + 'Uquest_initial.csv')
        
        a = compute_a_from_Uin_Uquest(Uin_ideal, Uquest_initial, 3)
        K_new = compute_K_from_a(a, verbosity=0)

        Uin_computed, Uquest_addapted = compute_Uin_from_Uquest(Uquest_initial, K_new, verbosity=0)

        Uin_computed.Vpp = Uin_computed.Vpp * 1.5
        Uin_ideal.Vpp = Uin_ideal.Vpp * 1.5

        Uin_computed_overlay_obj = overlay(Uin_computed, Uin_ideal)

        test_succeeded = finilize_tezt(values_computed=Uin_computed, set_accepted_values=0, verbosity=0)
        self.assertTrue(test_succeeded)
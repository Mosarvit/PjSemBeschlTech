import unittest
from unittest import TestCase

import numpy as np

from blocks.compute_Uquest_from_Uout import compute_Uquest_from_Uout
from helpers.csv_helper import read_in_signal
from helpers.csv_helper import read_in_transfer_function
from helpers.tezt_helper import finilize_tezt_with_signal
from settings import mock_data_path


class test_compute_Uquest_from_Uout(TestCase):

    def __init__(self, *args, **kwargs):
        super(test_compute_Uquest_from_Uout, self).__init__(*args, **kwargs)

    @unittest.skip("data not reasonable")
    def test_compute_Uquest_from_Uout_300_jens(self):

       Uout_300 = read_in_signal(mock_data_path + 'Uout_300_jens.csv')
       Uquest_300_ideal_matlab = read_in_signal(mock_data_path + 'Uquest_300_jens.csv')

       H = read_in_transfer_function(mock_data_path + 'H_jens.csv')

       Uquest_300_computed = compute_Uquest_from_Uout(Uout=Uout_300, H=H, verbosity=False)

       test_succeeded = finilize_tezt_with_signal(U_computed=Uquest_300_computed, set_ideal_signal=0, verbosity=0)
       self.assertTrue(test_succeeded)

    def test_compute_Uquest_from_Uout_300_our(self):
        Uout_300 = read_in_signal(mock_data_path + 'Uout_300_our.csv')
        Uquest_300_ideal_matlab = read_in_signal(mock_data_path + 'Uquest_300_our.csv')

        H = read_in_transfer_function(mock_data_path + 'H_our.csv')

        Uquest_300_computed = compute_Uquest_from_Uout(Uout=Uout_300, H=H, verbosity=False)

        test_succeeded = finilize_tezt_with_signal(U_computed=Uquest_300_computed, set_ideal_signal=0, verbosity=0)
        self.assertTrue(test_succeeded)

    def test_compute_Uquest_from_Uout_with_BBsignal_ideal(self):

        BBsignal_ideal = read_in_signal(mock_data_path + 'BBsignal_our.csv')
        Uquest_from_BBsignal_ideal = read_in_signal(mock_data_path + 'Uquest_from_BBsignal_our.csv')

        H = read_in_transfer_function(mock_data_path + 'H_our.csv')

        Uquest_from_BBsignal_computed = compute_Uquest_from_Uout(Uout=BBsignal_ideal, H=H, verbosity=False)

        test_succeeded = finilize_tezt_with_signal(U_computed=Uquest_from_BBsignal_computed, set_ideal_signal=0, verbosity=0)
        self.assertTrue(test_succeeded)



    # @unittest.skip("reason for skipping")
    def test_compute_Uquest_from_Uout_catch_imaginary(self):

        BBsignal_ideal = read_in_signal(mock_data_path + 'BBsignal_our.csv')

        H = read_in_transfer_function(mock_data_path + 'H_our.csv')

        Uquest_from_BBsignal_computed = compute_Uquest_from_Uout(Uout=BBsignal_ideal, H=H, verbosity=False)

        self.assertFalse(np.iscomplex(Uquest_from_BBsignal_computed.in_V.any()))
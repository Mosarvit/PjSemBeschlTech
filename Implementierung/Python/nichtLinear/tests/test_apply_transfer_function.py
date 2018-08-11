from unittest import TestCase

from blocks.generate_BBsignal import generate_BBsignal
from helpers.apply_transfer_function import apply_transfer_function
from helpers.csv_helper import read_in_signal
from helpers.csv_helper import read_in_transfer_function, read_in_transfer_function_old_convention
from helpers.overlay import overlay
from helpers.tezt_helper import finilize_tezt
from settings import mock_data_path


class test_apply_transfer_function(TestCase):

    def __init__(self, *args, **kwargs):
        super(test_apply_transfer_function, self).__init__(*args, **kwargs)


    def test_apply_transfer_function_BBsignal(self):

        H = read_in_transfer_function(mock_data_path + 'H_jens.csv')

        U_BBsignal_generated = generate_BBsignal()
        Uquest_300 = apply_transfer_function(U_BBsignal_generated, H.get_inverse())
        Uout_computed = apply_transfer_function(Uquest_300, H)
        Uout_computed = overlay(Uout_computed, U_BBsignal_generated)

        test_succeeded = finilize_tezt(values_computed=Uout_computed, set_accepted_values=0, verbosity=0)
        self.assertTrue(test_succeeded)


    def test_apply_transfer_function_2(self):

        H = read_in_transfer_function_old_convention(mock_data_path + 'adjustH/Messung3/Ha_0.csv',
                                                     mock_data_path + 'adjustH/Messung3/Hp_0.csv')

        Uout_300_ideal = read_in_signal(mock_data_path + 'Uout_300_our.csv')
        Uquest_300 = apply_transfer_function(Uout_300_ideal, H.get_inverse())
        Uout_computed = apply_transfer_function(Uquest_300, H)
        Uout_300_ideal = overlay(Uout_300_ideal, Uout_computed)

        test_succeeded = finilize_tezt(values_computed=Uout_computed, set_accepted_values=0, verbosity=0)
        self.assertTrue(test_succeeded)




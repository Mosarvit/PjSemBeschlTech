from unittest import TestCase

from helpers.csv_helper import get_current_unit_tezt_folder, read_in_transfer_function, read_in_K, read_in_a, \
    read_in_signal
from helpers.signal_helper import calculate_error
from settings import project_path
from blocks.loop_adjust_a import loop_adjust_a
from helpers.plot_helper import plot_K


class test_loop_adjust_a(TestCase):

    def __init__(self, *args, **kwargs):
        super(test_loop_adjust_a, self).__init__(*args, **kwargs)

    def test_loop_adjust_a_68(self):

        data_directory = project_path + 'tests/mock_data/mock_results/adjust_a/'

        current_folder = get_current_unit_tezt_folder()

        sample_rate_DSO = 9999e5

        Uout_ideal = read_in_signal(current_folder + 'Uout_ideal.csv')
        H_0 = read_in_transfer_function(current_folder + 'H_initial.csv')
        a_0 = read_in_a(current_folder + 'a_68.csv')
        K_0 = read_in_K(current_folder + 'K_68.csv')

        # plot_K(K_0)

        Uout_measured, quality_development, Ks = loop_adjust_a(a_0, K_0, H_0, Uout_ideal, data_directory,
                                                                  num_iters=10, sample_rate_DSO=sample_rate_DSO)

        self.assertTrue(1)



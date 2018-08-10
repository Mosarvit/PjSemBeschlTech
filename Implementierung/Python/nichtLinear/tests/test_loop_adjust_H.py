from unittest import TestCase

from helpers.csv_helper import get_current_unit_tezt_folder, read_in_transfer_function, read_in_K, read_in_a, \
    read_in_signal
from helpers.signal_helper import calculate_error
from settings import project_path, mock_system
from blocks.loop_adjust_a import loop_adjust_a
from blocks.loop_adjust_H import loop_adjust_H
from helpers.plot_helper import plot_K, plot_transfer_function, plot_2_transfer_functions, plot_H_ideal_Hs
from classes.transfer_function_class import transfer_function_class
from blocks.determine_a import determine_a
from blocks.compute_K_from_a import compute_K_from_a
from blocks.generate_BBsignal import generate_BBsignal


class test_loop_adjust_H(TestCase):

    def __init__(self, *args, **kwargs):
        super(test_loop_adjust_H, self).__init__(*args, **kwargs)

    def test_loop_adjust_H(self):

        data_directory = project_path + 'tests/mock_data/mock_results/adjust_H/'

        f_rep = 900e3
        f_BB = 5e6
        Vpp = 0.6

        sample_rate_AWG_max = 2e8
        sample_rate_DSO = 9999e5

        Uout_ideal = generate_BBsignal(f_rep=f_rep, f_BB=f_BB, Vpp=Vpp, sample_rate_AWG_max=sample_rate_AWG_max,
                                       verbosity=0)

        H_mock = mock_system.H
        H_0 = transfer_function_class(H_mock.f)
        H_0.a = H_mock.a * 1.05
        H_0.p = H_mock.p * 1.03

        a_0 = determine_a(H_0, Uout_ideal, sample_rate_DSO, data_directory)
        K_0 = compute_K_from_a(a=a_0, verbosity=0)

        # plot_2_transfer_functions(H_mock, H_0, legend1="$H_{mock}$", legend2="$H_{0}$");

        Hs, Uout_measured, quality_development= loop_adjust_H(H_0, K_0, Uout_ideal, data_directory,
                                                                  num_iters=10, sample_rate_DSO=sample_rate_DSO)

        # plot_H_ideal_Hs(H_mock, Hs)

        self.assertTrue(quality_development[1]>quality_development[-1] and quality_development[1]>quality_development[-2])



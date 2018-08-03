from unittest import TestCase

from scipy import linalg

from evaluate_adjust_a import evaluate_adjust_a
from helpers.overlay import overlay
from helpers.plot_helper import plot_2_signals, plot_2_transfer_functions, plot_3_transfer_functions, plot_3_Ks, plot_K_ideal_Ks
from helpers.signal_helper import calculate_error
from settings import mock_system


class test_evaluate_adjust_a(TestCase):

    def __init__(self, *args, **kwargs):
        super(test_evaluate_adjust_a, self).__init__(*args, **kwargs)

    def test_evaluate_adjust_a_0_steps(self):

        Uout_ideal, Uout_measured, Ks = evaluate_adjust_a(num_iters=1, verbosity=0)

        K_ideal = mock_system.K

        verbosity = 0
        if verbosity:
            plot_K_ideal_Ks(K_ideal, Ks)

        err = calculate_error(Ks[0], K_ideal)

        self.assertTrue(1)

    def test_evaluate_adjust_a_3_steps(self):

        Uout_ideal, Uout_measured, Ks = evaluate_adjust_a(num_iters=5, verbosity=0)

        K_ideal = mock_system.K

        verbosity = 0
        if verbosity:
            plot_K_ideal_Ks(K_ideal, Ks)

        err_0 = calculate_error(Ks[0], K_ideal)
        err_last = calculate_error(Ks[-1], K_ideal)

        self.assertTrue(err_last < err_0)



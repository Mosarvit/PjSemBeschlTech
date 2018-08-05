from unittest import TestCase

from scipy import linalg

from evaluate_adjust_H import evaluate_adjust_H
from helpers.overlay import overlay
from helpers.plot_helper import plot_2_signals, plot_2_transfer_functions, plot_3_transfer_functions, plot_H_ideal_Hs
from helpers.signal_helper import calculate_error
from settings import mock_system


class test_evaluate_adjust_H(TestCase):


    def __init__(self, *args, **kwargs):
        super(test_evaluate_adjust_H, self).__init__(*args, **kwargs)

    def test_evaluate_adjust_H_0_steps(self):

        Uout_ideal, Uout_measured, Hs = evaluate_adjust_H(num_iters=1, verbosity=0)

        H_ideal = mock_system.H

        verbosity = 0
        if verbosity:
            plot_H_ideal_Hs(H_ideal, Hs)
            plot_2_signals(Uout_ideal, Uout_measured, legend1='Uout_ideal', legend2='Uout_measured')

        err = calculate_error(Hs[0], H_ideal)

        self.assertTrue(err < 32e-2)


    def test_evaluate_adjust_H_5_steps(self):

        Uout_ideal, Uout_measured, Hs = evaluate_adjust_H(num_iters=5, verbosity=0)

        H_ideal = mock_system.H

        verbosity = 1
        if verbosity:
            plot_H_ideal_Hs(H_ideal, Hs)
            plot_2_signals(Uout_ideal, Uout_measured, legend1='Uout_ideal', legend2='Uout_measured')

        err_0 = calculate_error(Hs[0], H_ideal)
        err_last = calculate_error(Hs[-1], H_ideal)

        self.assertTrue(err_last < err_0)



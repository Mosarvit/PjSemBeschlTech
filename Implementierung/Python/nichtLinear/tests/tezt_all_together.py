from unittest import TestCase
import unittest
from numpy import genfromtxt
from scipy import linalg
import matplotlib.pyplot as plt
from blocks.adjust_H import adjust_H
from blocks.adjust_a import adjust_a

from helpers import overlay, signal_helper
from helpers.signal_helper import generateSinSum
from helpers.csv_helper import read_in_transfer_function
from classes.transfer_function_class import transfer_function_class
from helpers.apply_transfer_function import apply_transfer_function


from blocks.generate_BBsignal import generate_BBsignal
from blocks.compute_Uquest_from_Uout import compute_Uquest_from_Uout
from blocks.compute_K_from_a import compute_K_from_a
from blocks.compute_Uin_from_Uquest import compute_Uin_from_Uquest
from blocks.compute_a_from_Uin_Uquet import compute_a_from_Uin_Uquet
from settings import project_path, mock_data_path
from settings import mock_system
from blocks import get_H
import os
from classes.signal_class import signal_class
from helpers.csv_helper import read_in_signal, read_in_transfer_function, read_in_transfer_function_complex, read_in_transfer_function_old_convention
import evaluate_adjust_a, evaluate_adjust_H
from blocks.generate_BBsignal import generate_BBsignal_new, generate_BBsignal
from helpers.plot_helper import plot_2_signals, plot_2_transfer_functions

import numpy as np


class test_adjust_a(TestCase):

    def __init__(self, *args, **kwargs):
        super(test_adjust_a, self).__init__(*args, **kwargs)

    @unittest.skip("currently not working")
    def test_adjust_a(self):
        # erster Logik Test
        x = np.linspace(0,10)
        a_old = [0, 1, 0]

        u_ideal1 = np.zeros((len(x), 2))
        u_ideal2 = np.zeros((len(x), 2))
        u_ideal1[:, 0] = x
        u_ideal2[:, 0] = x
        u_ideal1[:, 1] = [np.power(xi, 2) for xi in x]
        u_ideal2[:, 1] = u_ideal1[:,1] + [2*np.power(xi, 3) for xi in x]
        a_new = adjust_a(a_old, x, u_ideal1, u_ideal2, 1)
        print(a_new)


        err = linalg.norm(0)

        self.assertTrue(err < 0.001) # we allow an error of 0.1% for the start, but it should be better

    def test_adjust_H_a_trivial(self):

        Halt = read_in_transfer_function(mock_data_path + 'H_jens.csv')

        Hneu_ideal = Halt

        t = np.linspace(0, .0001, 1000)
        Uout_ideal = generateSinSum(np.array([[1, 4], [2, 6], [3, 10]], np.int32), t)
        Uout_measured = Uout_ideal

        sigma_H = 0.5

        Hneu = adjust_H(Halt, Uout_ideal, Uout_measured, sigma_H)

        err = linalg.norm(Hneu.a - Hneu_ideal.a) / linalg.norm(Hneu_ideal.a)
        self.assertTrue(err < 0.001)

    def test_adjust_H_p_trivial(self):

        """
        trivial test:
        if
          Uout_measured = Uout_ideal
        than
          Hneu = Halt
        """

        Halt = read_in_transfer_function(mock_data_path + '/H_jens.csv')
        Hneu_ideal = Halt

        t = np.linspace(0, 1e-5, 1000)
        Uout_ideal = generateSinSum(np.array([[1, 4], [2, 6], [3, 10]], np.int32), t)
        Uout_measured = Uout_ideal

        sigma_H = 0.5

        Hneu = adjust_H(Halt, Uout_ideal, Uout_measured, sigma_H)

        err = linalg.norm(Hneu.c - Hneu_ideal.c) / linalg.norm(Hneu_ideal.c)
        self.assertTrue(err < 0.001)

    def test_adjust_H_sinus(self):

        """
        if
          Uout_ideal is a sum of three sin functions
          Uout_measured = 2 * Uout_ideal
          sigma_H = 0.5,
        than
          Hneu.a = Halt.a * 1.5
        """

        verbosity = 0

        Halt = read_in_transfer_function(mock_data_path + 'H_jens.csv')
        Hneu_ideal = transfer_function_class(Halt.f)

        sigma_H = 0.5
        factor = 2
        Hneu_ideal.a = Halt.a * (1 - ((factor - 1) * sigma_H))
        Hneu_ideal.p = Halt.p
        # Tmax = 3e-6 # will not suceed: too little frequencies in spectrum of Uout_ideal
        Tmax = 3e-7  # will suceed: wide frequencie range in spectrum of Uout_ideal
        F_sample = 4 * Halt.f[-1]
        N = int(np.ceil(Tmax * F_sample))
        if verbosity:
            print(N)
        t = np.linspace(0, Tmax, N)
        if verbosity:
            print('delta t' + str(t[1] - t[0]))
        # Do not change Signal because for above used formula signal has to contain every frequency possible
        Uout_ideal = generateSinSum(np.array([[1, 4], [2, 6], [3, 10]]), t)

        Uout_measured = signal_class(Uout_ideal.time, Uout_ideal.in_V * factor)

        # Uout_measured = np.zeros((Uout_ideal.length, 2))
        # Uout_measured[:, 0] = Uout_ideal[:, 0]
        # Uout_measured[:, 1] = [x * factor for x in Uout_ideal[:, 1]]

        Hneu = adjust_H(Halt, Uout_ideal, Uout_measured, sigma_H, verbosity=verbosity)

        # this will never work: see plots, range of frequencies in signals is to low because of too little number of points
        err = linalg.norm(Hneu.c - Hneu_ideal.c) / linalg.norm(Hneu_ideal.c)

        self.assertTrue(err < 0.001)  # we allow an error of 0.1% for the start, but it should be better

    def test_adjust_H(self):

        """
                if
                  Uout_ideal is a BB Signal
                  Uout_measured = 2 * Uout_ideal
                  sigma_H = 0.5,
                than
                  Hneu.a = Halt.a * 1.5
                but:
                """
        # Initialization
        factor = 2
        sigma_H = 0.5
        # initalize BB signal
        f_rep = 900e3
        f_BB = 5e6
        Vpp = 0.3

        sample_rate_AWG_max = 2e8
        sample_rate_DSO = 9999e5

        Uout_ideal = generate_BBsignal(f_rep=f_rep, f_BB=f_BB, Vpp=Vpp, sample_rate_AWG_max=sample_rate_AWG_max)

        Halt = read_in_transfer_function_old_convention(mock_data_path + 'adjustH/Messung2/Ha_0.csv',
                                                        mock_data_path + 'adjustH/Messung2/Hp_0.csv')
        Hneu_ideal = transfer_function_class(Halt.f)
        Hneu_ideal.a = Halt.a * (1 - sigma_H * (factor - 1))
        Hneu_ideal.p = Halt.p

        # to illustrate function of adjust_H: testcase 1 to run (and finish) test, 2 to show plots of adjusting calculated H
        testcase = 1
        if testcase == 1:
            Uout_measured = signal_class(Uout_ideal.time, Uout_ideal.in_V * 2)
            # Uout_measured = np.zeros((Uout_ideal.shape[0], 2))
            # Uout_measured[:, 0] = Uout_ideal[:, 0]
            # Uout_measured[:, 1] = [x * 2 for x in Uout_ideal[:, 1]]
        else:
            ## to show pictures of first step of adjust_H in real application instead of testing
            Uout_measured = read_in_signal(mock_data_path + 'adjustH/Messung2/Uout_1.csv')

        def to_test():
            Hneu = adjust_H(Halt, Uout_ideal, Uout_measured, sigma_H=sigma_H, verbosity=0)
            return

        # t = timeit.timeit(to_test, number=1)
        # print("Laufzeit adjust_H in milli Sec: " + str(t * 1e3))
        Hneu = adjust_H(Halt, Uout_ideal, Uout_measured, sigma_H=sigma_H, verbosity=0)

        err = linalg.norm(Hneu.c - Hneu_ideal.c) / linalg.norm(Hneu_ideal.c)
        self.assertTrue(err < 0.00001)  # we allow an error of 0.1% for the start, but it should be better

    def test_adjust_H_p_trivial(self):

        """
        trivial test:
        if
          Uout_measured = Uout_ideal
        than
          Hneu = Halt
        """

        Halt = read_in_transfer_function(mock_data_path + 'H_jens.csv')
        Hneu_ideal = Halt

        t = np.linspace(0, 1e-5, 1000)
        Uout_ideal = generateSinSum(np.array([[1, 4], [2, 6], [3, 10]], np.int32), t)
        Uout_measured = Uout_ideal

        sigma_H = 0.5

        Hneu = adjust_H(Halt, Uout_ideal, Uout_measured, sigma_H)

        err = linalg.norm(Hneu.c - Hneu_ideal.c) / linalg.norm(Hneu_ideal.c)
        self.assertTrue(err < 0.001)

    @unittest.skip("old version")
    def test_adjust_H1(self):

        """
                if
                  Uout_ideal is a BB Signal
                  Uout_measured = 2 * Uout_ideal
                  sigma_H = 0.5,
                than
                  Hneu.a = Halt.a * 1.5
                but:
                """
        # Initialization
        factor = 2
        sigma_H = 0.5
        # initalize BB signal
        sampleRateDSO = 999900000
        f_rep = 900e3
        sample_rate_AWG_max = 223 * f_rep
        f_BB = 5e6
        Vpp = 0.3
        Uout_ideal = generate_BBsignal(f_rep=f_rep, f_BB=f_BB, Vpp=Vpp, sample_rate_AWG_max=sample_rate_AWG_max,
                                       saveCSV=False, verbosity=0)
        Uout_ideal = Uout_ideal.get_signal_in_V_old_convention()

        Halt = read_in_transfer_function_old_convention(mock_data_path + 'adjustH/Messung2/Ha_0.csv',
                                                        mock_data_path + 'adjustH/Messung2/Hp_0.csv')
        Hneu_ideal = transfer_function_class(Halt.f)
        Hneu_ideal.a = Halt.a * (1 + sigma_H * (factor - 1))
        Hneu_ideal.p = Halt.p

        # to illustrate function of adjust_H: testcase 1 to run (and finish) test, 2 to show plots of adjusting calculated H
        testcase = 2
        if testcase == 1:
            Uout_measured = np.zeros((Uout_ideal.shape[0], 2))
            Uout_measured[:, 0] = Uout_ideal[:, 0]
            Uout_measured[:, 1] = [x * 2 for x in Uout_ideal[:, 1]]
        else:
            ## to show pictures of first step of adjust_H in real application instead of testing
            Uout_measured = genfromtxt(mock_data_path + 'adjustH/Messung2/Uout_1.csv', delimiter=',')

        Hneu = adjust_H(Halt, Uout_ideal, Uout_measured, sigma_H=sigma_H, verbosity=True)

        err = linalg.norm(Hneu.c - Hneu_ideal.c) / linalg.norm(Hneu_ideal.c)
        self.assertTrue(err < 0.00001)  # we allow an error of 0.1% for the start, but it should be better

    def test_apply_transfer_function_BBsignal(self):

        H = read_in_transfer_function(mock_data_path + 'H_jens.csv')

        Uout_300_ideal = generate_BBsignal()
        Uquest_300 = apply_transfer_function(Uout_300_ideal, H.get_inverse())
        Uout_computed = apply_transfer_function(Uquest_300, H)

        err = linalg.norm(Uout_computed.in_V - Uout_300_ideal.in_V) / linalg.norm(Uout_300_ideal.in_V)

        self.assertTrue(err < 0.03)

    def test_apply_transfer_function(self):

        H = read_in_transfer_function(mock_data_path + 'H_jens.csv')

        Uout_300_ideal = read_in_signal(mock_data_path + 'Uout_300_jens.csv')
        # Uout_300_ideal = Uout_300_ideal.get_signal_in_V_old_convention()
        Uquest_300 = apply_transfer_function(Uout_300_ideal, H.get_inverse())
        Uout_computed = apply_transfer_function(Uquest_300, H)

        err = linalg.norm(Uout_computed.in_V - Uout_300_ideal.in_V) / linalg.norm(Uout_300_ideal.in_V)

        self.assertTrue(err < 0.04)

    def test_apply_transfer_function_2(self):

        H = read_in_transfer_function_old_convention(mock_data_path + 'adjustH/Messung3/Ha_0.csv',
                                                     mock_data_path + 'adjustH/Messung3/Hp_0.csv')

        Uout_300_ideal = read_in_signal(mock_data_path + 'Uout_300_jens.csv')
        # Uout_300_ideal = Uout_300_ideal.get_signal_in_V_old_convention()
        Uquest_300 = apply_transfer_function(Uout_300_ideal, H.get_inverse())
        Uout_computed = apply_transfer_function(Uquest_300, H)

        err = linalg.norm(Uout_computed.in_V - Uout_300_ideal.in_V) / linalg.norm(Uout_300_ideal.in_V)

        self.assertTrue(err < 0.04)

    @unittest.skip(
        "The mock data cannot be correct, since the timeperiod of Uquest_300_jens.csv and Uin_jens.csv are too different")
    def test_compute_a_from_Uin_Uquest_300_jens(self):
        Uquest_300 = read_in_signal(mock_data_path + 'Uquest_300_jens.csv')
        Uin = read_in_signal(mock_data_path + 'Uin_jens.csv')
        Uin.Vpp = 0.3

        a_300_ideal = genfromtxt(mock_data_path + 'a_300_jens.csv', delimiter=',')

        a_300_computed = compute_a_from_Uin_Uquet(Uin=Uin, Uquest=Uquest_300, N=3)

        err = linalg.norm(a_300_computed - a_300_ideal) / linalg.norm(a_300_ideal)
        self.assertTrue(err < 1e-3)

    def test_compute_a_from_Uin_Uquest_300_our(self):
        Uquest_300 = read_in_signal(mock_data_path + 'Uquest_300_our.csv')
        Uin = read_in_signal(mock_data_path + 'Uin_our.csv')
        Uin.Vpp = 0.3

        a_300_ideal = genfromtxt(mock_data_path + 'a_300_our.csv', delimiter=',')

        a_300_computed = compute_a_from_Uin_Uquet(Uin=Uin, Uquest=Uquest_300, N=3)

        err = linalg.norm(a_300_computed - a_300_ideal) / linalg.norm(a_300_ideal)
        self.assertTrue(err < 1e-3)

    def test_compute_K_from_a_jens(self):
        K_300_ideal = genfromtxt(mock_data_path + 'K_300_jens.csv', delimiter=',')

        a_300 = genfromtxt(mock_data_path + 'a_300_jens.csv', delimiter=',')

        K_computed = compute_K_from_a(a_300, verbosity=False)

        err = linalg.norm(K_computed - K_300_ideal) / linalg.norm(K_300_ideal)
        self.assertTrue(err < 1e-3)

    def test_compute_K_from_a_our(self):
        K_300_ideal = genfromtxt(mock_data_path + 'K_300_our.csv', delimiter=',')

        a_300 = genfromtxt(mock_data_path + 'a_300_our.csv', delimiter=',')

        K_computed = compute_K_from_a(a_300, verbosity=False)

        err = linalg.norm(K_computed - K_300_ideal) / linalg.norm(K_300_ideal)
        self.assertTrue(err < 1e-3)

 # @unittest.skip("reason for skipping")
    def test_compute_Uin_from_Uquest_jens(self):

        Uin_ideal = read_in_signal(mock_data_path + 'Uin_jens.csv')
        Uin_ideal.Vpp = 0.3

        Uquest_300 = read_in_signal(mock_data_path + 'Uquest_300_jens.csv')

        K_300 = genfromtxt(mock_data_path + 'K_300_jens.csv', delimiter=',')

        Uin_computed = compute_Uin_from_Uquest(Uquest_300, K_300, verbosity=False)

        Uin_computed_overlay_obj = overlay.overlay(Uin_computed, Uin_ideal)


        # plt.figure()
        # plt.plot(Uin_computed_overlay_obj.time, Uin_computed_overlay_obj.in_V)
        # plt.plot(Uin_ideal.time, Uin_ideal.in_V)
        # plt.legend(['Uin_computed_overlay_obj', 'Uin_ideal'])
        # plt.xlabel('t')
        # plt.ylabel('U')
        # if global_data.showPlots:
        #     plt.show()

        err = linalg.norm(Uin_computed_overlay_obj.in_V - Uin_ideal.in_V) / linalg.norm(Uin_ideal.in_V)
        self.assertTrue(err < 0.2)

    def test_compute_Uin_from_Uquest_our(self):

        Uin_ideal = read_in_signal(mock_data_path + 'Uin_our.csv')
        Uin_ideal.Vpp = 0.3

        Uquest_300 = read_in_signal(mock_data_path + 'Uquest_300_our.csv')

        K_300 = genfromtxt(mock_data_path + 'K_300_jens.csv', delimiter=',')

        Uin_computed = compute_Uin_from_Uquest(Uquest_300, K_300, verbosity=False)

        Uin_computed_overlay_obj = overlay.overlay(Uin_computed, Uin_ideal)

        err = linalg.norm(Uin_computed_overlay_obj.in_V - Uin_ideal.in_V) / linalg.norm(Uin_ideal.in_V)
        self.assertTrue(err < 0.2)

    def test_compute_Uin_from_Uquest_air(self):

        path = mock_data_path + 'adjust_a_19_07_2018-14_02_41/'

        Uin_awg = read_in_signal(path + 'Uin_initial.csv')
        Uquest_initial = read_in_signal(path + 'Uquest_initial.csv')
        K_300 = genfromtxt(path + 'K_initial.csv', delimiter=',')

        Uin_computed = compute_Uin_from_Uquest(Uquest_initial, K_300, verbosity=False)

        Uin_computed_overlay_obj = overlay.overlay(Uin_computed, Uin_awg)

        err = linalg.norm(Uin_computed_overlay_obj.in_V - Uin_awg.in_V) / linalg.norm(Uin_awg.in_V)
        self.assertTrue(err < 0.2)


    def test_compute_Uin_from_Uquest_air(self):

        path = mock_data_path + 'adjust_a_19_07_2018-14_02_41/'

        Uin_awg = read_in_signal(path + 'Uin_initial.csv')
        Uquest_initial = read_in_signal(path + 'Uquest_initial.csv')
        K_300 = genfromtxt(path + 'K_initial.csv', delimiter=',')

        Uin_computed = compute_Uin_from_Uquest(Uquest_initial, K_300, verbosity=False)

        Uin_computed_overlay_obj = overlay.overlay(Uin_computed, Uin_awg)

        err = linalg.norm(Uin_computed_overlay_obj.in_V - Uin_awg.in_V) / linalg.norm(Uin_awg.in_V)
        self.assertTrue(err < 0.2)

    def test_compute_Uin_from_Uquest_from_adjust_a(self):

        path = mock_data_path + 'adjust_a_19_07_2018-13_53_38/'

        Uin_awg = read_in_signal(path + 'Uin_initial.csv')
        Uquest_initial = read_in_signal(path + 'Uquest_initial.csv')
        K_300 = genfromtxt(path + 'K_initial.csv', delimiter=',')

        Uin_computed = compute_Uin_from_Uquest(Uquest_initial, K_300, verbosity=False)

        Uin_computed_overlay_obj = overlay.overlay(Uin_computed, Uin_awg)

        err = linalg.norm(Uin_computed_overlay_obj.in_V - Uin_awg.in_V) / linalg.norm(Uin_awg.in_V)
        self.assertTrue(err < 0.2)

    def test_compute_Uquest_from_Uout_300_jens(self):

        Uout_300 = read_in_signal(mock_data_path + 'Uout_300_jens.csv')
        Uquest_300_ideal = read_in_signal(mock_data_path + 'Uquest_300_jens.csv')

        H = read_in_transfer_function(mock_data_path + 'H_jens.csv')

        Uquest_300_computed = compute_Uquest_from_Uout(Uout=Uout_300, H=H, verbosity=False)

        err = linalg.norm(Uquest_300_computed.in_V - Uquest_300_ideal.in_V) / linalg.norm( Uquest_300_ideal.in_V)
        self.assertTrue(err < 0.03)

    def test_compute_Uquest_from_Uout_300_our(self):
        Uout_300 = read_in_signal(mock_data_path + 'Uout_300_our.csv')
        Uquest_300_ideal = read_in_signal(mock_data_path + 'Uquest_300_our.csv')

        H = read_in_transfer_function(mock_data_path + 'H_our.csv')

        Uquest_300_computed = compute_Uquest_from_Uout(Uout=Uout_300, H=H, verbosity=False)

        err = linalg.norm(Uquest_300_computed.in_V - Uquest_300_ideal.in_V) / linalg.norm(Uquest_300_ideal.in_V)
        self.assertTrue(err < 0.03)

    def test_compute_Uquest_from_Uout_with_BBsignal_ideal(self):

        BBsignal_ideal = read_in_signal(mock_data_path + 'BBsignal_our.csv')
        Uquest_from_BBsignal_ideal = read_in_signal(mock_data_path + 'Uquest_from_BBsignal_our.csv')

        H = read_in_transfer_function(mock_data_path + 'H_our.csv')

        Uquest_from_BBsignal_computed = compute_Uquest_from_Uout(Uout=BBsignal_ideal, H=H, verbosity=False)

        err = linalg.norm(Uquest_from_BBsignal_computed.in_V - Uquest_from_BBsignal_ideal.in_V) / linalg.norm(Uquest_from_BBsignal_ideal.in_V)
        self.assertTrue(err<0.04)



    # @unittest.skip("reason for skipping")
    def test_compute_Uquest_from_Uout_catch_imaginary(self):

        BBsignal_ideal = read_in_signal(mock_data_path + 'BBsignal_our.csv')

        H = read_in_transfer_function(mock_data_path + 'H_our.csv')

        Uquest_from_BBsignal_computed = compute_Uquest_from_Uout(Uout=BBsignal_ideal, H=H, verbosity=False)

        self.assertFalse(np.iscomplex(Uquest_from_BBsignal_computed.in_V.any()))


    # @unittest.skip("currently not relevant")
    def test_evaluate_adjust_H_0_steps(self):

        Uout_ideal, Uout_measured, _, _ = evaluate_adjust_H(num_iters=1, verbosity=0)

        Uout_measured = overlay(Uout_measured, Uout_ideal)

        err = linalg.norm(Uout_measured.in_V - Uout_ideal.in_V) / linalg.norm(Uout_ideal.in_V)

        verbosity = 0
        if verbosity :
            plot_2_signals(Uout_ideal, Uout_measured, 'Uout_measured', 'Uout_ideal')

        self.assertTrue(err < 0.07)


    def test_evaluate_adjust_H_1_step(self):

        Uout_ideal, Uout_measured, H_0, H_last = evaluate_adjust_H(num_iters=5, verbosity=0)

        err = linalg.norm(H_0.a - H_last.a) / linalg.norm(H_last.a)

        verbosity = 0

        if verbosity :
            plot_2_transfer_functions(H_0, H_last, 'H_0', 'H_last')

        self.assertTrue(err < 0.02)


    @unittest.skip("currently not working")
    def test_generate_BBsignal_show(self):
        # Initialization
        sampleRateDSO = 999900000
        f_rep = 900e3
        sample_rate_AWG_max = 223 * f_rep
        f_BB = 5e6
        Vpp = 0.3
        Uout_ideal = generate_BBsignal(f_rep=f_rep, f_BB=f_BB, Vpp=Vpp, sample_rate_AWG_max=sample_rate_AWG_max,
                                   saveCSV=True, verbosity=False)

        Uout_2 = generate_BBsignal_new(f_rep=f_rep, f_BB=f_BB, Vpp=Vpp, sample_rate_AWG_max=sample_rate_AWG_max,
                                   saveCSV=True, verbosity=False)

        # print("Werte alt:")
        # signal_evaluate(settings.project_path + '/data/current_data/BBsignal_ideal.csv')
        # print("Werte neu:")
        # signal_evaluate(settings.project_path + '/data/current_data/BBsignal_new.csv')
        # Wirft fehler!

        self.assertTrue(True)


    @unittest.skip("currently not working")
    def test_get_H(self):


        H_ideal = read_in_transfer_function_old_convention(pathA = mock_data_path + 'ideal_12_07_2018_12_03_47/csv/HAmpl_linear.csv',
                                                     pathPh = mock_data_path + 'ideal_12_07_2018_12_03_47/csv/PhaseH.csv', delimiter=';')




        mock_system.H = H_ideal



        fmax = 80e6
        vpp = 40e-3
        bits = 9
        f, Ha, Hph = get_H.compute(fmax, vpp, bits=bits, showPlots=0)

        from settings import last_directory_used

        # Uin_comp_ideal = read_in_transfer_function_old_convention(path = mock_data_path + 'ideal_12_07_2018_12_03_47/csv/UinFrq.csv', delimiter=';')
        Uin_compl_ideal = read_in_transfer_function_old_convention(
            mock_data_path + 'ideal_12_07_2018_12_03_47/csv/UinAmplFrq_linear.csv', pathPh=last_directory_used + 'UinPhase.csv',
            delimiter=';')
        Uin_compl_computed = read_in_transfer_function_old_convention(pathA=last_directory_used + 'UinAmplFrq_linear.csv',  pathPh=last_directory_used + 'UinPhase.csv',delimiter=';')

        # plot_2_transfer_functions(H1=Uin_compl_ideal, H2=Uin_compl_computed, legend1='Uin_compl_ideal', legend2='Uin_compl_computed')
        # plot_transfer_function(H=Uin_compl_computed, legend1="Uin_compl_computed")

        Uin_ideal = read_in_signal(path = mock_data_path + 'ideal_12_07_2018_12_03_47/csv/UinTime.csv', delimiter=';')
        Uin_computed = read_in_signal(path = last_directory_used + 'UinTime.csv', delimiter=';')

        # plot_2_signals(U1=Uin_ideal, U2=Uin_computed, legend1='Uin_ideal', legend2='Uin_computed')

        Uout_ideal = read_in_signal(path = mock_data_path + 'ideal_12_07_2018_12_03_47/csv/UoutTime.csv', delimiter=';')
        Uout_computed = read_in_signal(path = last_directory_used + 'UoutTime.csv', delimiter=';')

        # plot_2_signals(U1=Uout_ideal, U2=Uout_computed, legend1='Uout_ideal', legend2='Uout_computed')



        H_determined = transfer_function_class(f)
        H_determined.a = Ha
        H_determined.p = Hph

        # plot_2_transfer_functions(H1=H_ideal, H2=H_determined, legend1='H_ideal', legend2='H_determined')

        self.assertTrue(1)


    def test_mock_system(self):
        sample_rate_DSO = 9999e5

        Uout_ideal = read_in_signal(mock_data_path + 'Uout_300_our.csv')
        Uquest_ideal = read_in_signal(mock_data_path + 'Uquest_300_our.csv')

        # sample_rate_DSO = Uquest_ideal.sample_rate

        mock_system.H = read_in_transfer_function(mock_data_path + 'H_our.csv')

        mock_system.write_to_AWG(signal=Uquest_ideal.in_V, awg_Vpp=Uquest_ideal.Vpp, samplerateAWG=Uout_ideal.sample_rate)
        time, dataUin, dataUout = mock_system.read_from_DSO(samplerateOszi=sample_rate_DSO, signal=Uquest_ideal, fmax=8e7,
                                                            vpp_ch1=Uquest_ideal.Vpp)

        Uout_computed = signal_class(time, dataUout)

        Uout_computed = overlay(Uout_computed, Uout_ideal)

        # plot_2_signals(Uout_ideal, Uout_computed)

        err = linalg.norm(Uout_computed.in_V - Uout_ideal.in_V) / linalg.norm(Uout_ideal.in_V)

        self.assertTrue(err < 0.04)


        if __name__ == '__main__':
            try:
                unittest.main()
            except SystemExit as inst:
                if inst.args[0] is True:  # raised by sys.exit(True) when tests failed
                    raise


    def test_setSampleRate(self):
        Uin = genfromtxt(mock_data_path + 'Uin_jens.csv', delimiter=',')

        sampleRate = 1e9

        T = max(Uin[:, 0]) - min(Uin[:, 0])
        lenght_new = int(np.floor(T * sampleRate))

        Uin_computed = signal_helper.set_sample_rate(Uin, sampleRate);

        self.assertTrue(Uin_computed.shape[0] == lenght_new)
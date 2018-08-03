import timeit
import unittest
from unittest import TestCase

import numpy as np
from numpy import genfromtxt
from scipy import linalg

from blocks.adjust_H import adjust_H
from blocks.generate_BBsignal import generate_BBsignal
from classes.signal_class import signal_class
from classes.transfer_function_class import transfer_function_class
from helpers.csv_helper import read_in_signal
from helpers.csv_helper import read_in_transfer_function, read_in_transfer_function_old_convention
from helpers.signal_helper import generateSinSum
from helpers.tezt_helper import finilize_tezt
from settings import mock_data_path


class test_adjust_H(TestCase):


    def __init__(self, *args, **kwargs):
        super(test_adjust_H, self).__init__(*args, **kwargs)

    def test_adjust_H_a_trivial(self):

        Halt = read_in_transfer_function(mock_data_path + 'H_jens.csv')

        Hneu_ideal = Halt

        t = np.linspace(0, .0001, 1000)
        Uout_ideal = generateSinSum(np.array([[1, 4], [2, 6], [3, 10]], np.int32), t)
        Uout_measured = Uout_ideal

        sigma_H = 0.5

        Hneu = adjust_H(Halt, Uout_ideal, Uout_measured, sigma_H)

        test_succeeded = finilize_tezt(values_computed=Hneu, set_ideal_values=0, verbosity=0)
        self.assertTrue(test_succeeded)

    def test_adjust_H_p_trivial(self):

        """
        trivial test:
        if
          Uout_measured = U_ideal.csv.csv.csv.csv
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

        test_succeeded = finilize_tezt(values_computed=Hneu, set_ideal_values=0, verbosity=0)
        self.assertTrue(test_succeeded)


    def test_adjust_H_sinus(self):

        """
        if
          U_ideal.csv.csv.csv.csv is a sum of three sin functions
          Uout_measured = 2 * U_ideal.csv.csv.csv.csv
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
        # Tmax = 3e-6 # will not suceed: too little frequencies in spectrum of U_ideal.csv.csv.csv.csv
        Tmax = 3e-7  # will suceed: wide frequencie range in spectrum of U_ideal.csv.csv.csv.csv
        F_sample = 4 * Halt.f[-1]
        N = int(np.ceil(Tmax * F_sample))
        if verbosity :
            print(N)
        t = np.linspace(0, Tmax, N)
        if verbosity:
            print('delta t' + str(t[1] - t[0]))
        # Do not change Signal because for above used formula signal has to contain every frequency possible
        Uout_ideal = generateSinSum(np.array([[1, 4], [2, 6], [3, 10]]), t)

        Uout_measured = signal_class(Uout_ideal.time, Uout_ideal.in_V * factor)

        # Uout_measured = np.zeros((U_ideal.csv.csv.csv.csv.length, 2))
        # Uout_measured[:, 0] = U_ideal.csv.csv.csv.csv[:, 0]
        # Uout_measured[:, 1] = [x * factor for x in U_ideal.csv.csv.csv.csv[:, 1]]

        Hneu = adjust_H(Halt, Uout_ideal, Uout_measured, sigma_H, verbosity=verbosity)

        test_succeeded = finilize_tezt(values_computed=Hneu, set_ideal_values=0, verbosity=0)
        self.assertTrue(test_succeeded)

    def test_adjust_H(self):

        """
                if
                  U_ideal.csv.csv.csv.csv is a BB Signal
                  Uout_measured = 2 * U_ideal.csv.csv.csv.csv
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
            # Uout_measured = np.zeros((U_ideal.csv.csv.csv.csv.shape[0], 2))
            # Uout_measured[:, 0] = U_ideal.csv.csv.csv.csv[:, 0]
            # Uout_measured[:, 1] = [x * 2 for x in U_ideal.csv.csv.csv.csv[:, 1]]
        else:
            ## to show pictures of first step of adjust_H in real application instead of testing
            Uout_measured = read_in_signal(mock_data_path + 'adjustH/Messung2/Uout_1.csv')

        def to_test():
            Hneu = adjust_H(Halt, Uout_ideal, Uout_measured, sigma_H=sigma_H, verbosity=0)
            return
        t = timeit.timeit(to_test, number=1)
        print("Laufzeit adjust_H in milli Sec: " + str(t*1e3))
        Hneu = adjust_H(Halt, Uout_ideal, Uout_measured, sigma_H=sigma_H, verbosity=0)

        test_succeeded = finilize_tezt(values_computed=Hneu, set_ideal_values=0, verbosity=0)
        self.assertTrue(test_succeeded)


    def test_adjust_H_p_trivial(self):

        """
        trivial test:
        if
          Uout_measured = U_ideal.csv.csv.csv.csv
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

        test_succeeded = finilize_tezt(values_computed=Hneu, set_ideal_values=0, verbosity=0)
        self.assertTrue(test_succeeded)

    @unittest.skip("old version")
    def test_adjust_H1(self):

        """
                if
                  U_ideal.csv.csv.csv.csv is a BB Signal
                  Uout_measured = 2 * U_ideal.csv.csv.csv.csv
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
        Uout_ideal = generate_BBsignal(f_rep=f_rep, f_BB=f_BB, Vpp=Vpp, sample_rate_AWG_max=sample_rate_AWG_max, saveCSV=False, verbosity=0)
        Uout_ideal = Uout_ideal.get_signal_in_V_old_convention()

        Halt = read_in_transfer_function_old_convention (mock_data_path + 'adjustH/Messung2/Ha_0.csv',
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

        test_succeeded = finilize_tezt(values_computed=Hneu, set_ideal_values=0, verbosity=0)
        self.assertTrue(test_succeeded)


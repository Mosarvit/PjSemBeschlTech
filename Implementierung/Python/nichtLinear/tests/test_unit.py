from unittest import TestCase
from numpy import genfromtxt
from scipy import linalg
from blocks.compute_Uquest_from_Uout import compute_Uquest_from_Uout
from blocks.compute_K_from_a import compute_K_from_a
from blocks.compute_Uin_from_Uquest import compute_Uin_from_Uquest
from blocks.compute_a_from_Uin_Uquet import compute_a_from_Uin_Uquet
from blocks.adjust_H import adjust_H
from blocks.adjust_a import adjust_a
from blocks.generate_BBsignal import generate_BBsignal
import matplotlib.pyplot as plt

from helpers import overlay, signalHelper
from helpers.signalHelper import generateSinSum
from helpers.csvHelper import read_in_transfer_function, read_in_transfer_function_old
from adts.transfer_function import transfer_function

import numpy as np


class test_unit(TestCase):

    global fixPath # fuer den Fall, dass er H.csv nicht finden kann
    fixPath = '../'
    # fixPath = ''

    def __init__(self, *args, **kwargs):
        super(test_unit, self).__init__(*args, **kwargs)
        # self.getHFromCSV()

    # def getHFromCSV(self):
    #
    #     Ha = genfromtxt(fixPath + 'data/test_data/H_a.csv', delimiter=',')
    #     Hph = genfromtxt(fixPath + 'data/test_data/H_p.csv', delimiter=',')
    #
    #     self.H = np.zeros(((Ha.shape[0]),3))
    #     self.H[:, 0:2] = Ha
    #     self.H[:, 2] = Hph[:, 1]
    #
    # def getComplexHFromCSV(self):
    #     str_H = np.genfromtxt(fixPath + 'data/test_data/H.csv', dtype=str, delimiter=',')
    #     self.H_ = np.zeros((len(str_H)), dtype=complex)
    #     self.freqA = np.zeros((len(str_H)))
    #     for k in range(0, len(str_H)):
    #         self.H_[k] = np.complex(str_H[k, 1].replace('i', 'j'))
    #         self.freqA[k] = float(str_H[k, 0])

    def test_compute_Uquest_from_Uout_300_jens(self):

       Uout_300 = genfromtxt(fixPath + 'data/test_data/Uout_300_jens.csv', delimiter=',')
       Uquest_300_ideal = genfromtxt(fixPath + 'data/test_data/Uquest_300_jens.csv', delimiter=',')

       H = read_in_transfer_function(fixPath + 'data/test_data/H_jens.csv')

       Uquest_300_computed = compute_Uquest_from_Uout(Uout=Uout_300, H=H, verbosity=False)

       err = linalg.norm(Uquest_300_computed[:,1] - Uquest_300_ideal[:,1]) / linalg.norm( Uquest_300_ideal[:,1])
       self.assertTrue(err < 0.03)



    def test_compute_Uquest_from_Uout_300_our(self):
        Uout_300 = genfromtxt(fixPath + 'data/test_data/Uout_300_our.csv', delimiter=',')
        Uquest_300_ideal = genfromtxt(fixPath + 'data/test_data/Uquest_300_our.csv', delimiter=',')

        H = read_in_transfer_function(fixPath + 'data/test_data/H_our.csv')

        Uquest_300_computed = compute_Uquest_from_Uout(Uout=Uout_300, H=H, verbosity=False)

        err = linalg.norm(Uquest_300_computed[:, 1] - Uquest_300_ideal[:, 1]) / linalg.norm(Uquest_300_ideal[:, 1])
        self.assertTrue(err < 0.03)

    def test_compute_Uquest_from_Uout_with_BBsignal_ideal(self):

        BBsignal_ideal = genfromtxt(fixPath + 'data/test_data/BBsignal_ideal.csv', delimiter=',')
        Uquest_from_BBsignal_ideal = genfromtxt(fixPath + 'data/test_data/Uquest_from_BBsignal_our.csv', delimiter=',')

        H = read_in_transfer_function(fixPath + 'data/test_data/H_our.csv')

        Uquest_from_BBsignal_computed = compute_Uquest_from_Uout(Uout=BBsignal_ideal, H=H, verbosity=False)

        err = linalg.norm(Uquest_from_BBsignal_computed[:,1] - Uquest_from_BBsignal_ideal[:,1]) / linalg.norm(Uquest_from_BBsignal_ideal[:,1])
        self.assertTrue(err<0.04)

    # @unittest.skip("reason for skipping")
    def test_compute_Uquest_from_Uout_catch_imaginary(self):

        BBsignal_ideal = genfromtxt(fixPath + 'data/test_data/BBsignal_ideal.csv', delimiter=',')

        H = read_in_transfer_function(fixPath + 'data/test_data/H_our.csv')

        Uquest_from_BBsignal_computed = compute_Uquest_from_Uout(Uout=BBsignal_ideal, H=H, verbosity=False)

        self.assertFalse(np.iscomplex(Uquest_from_BBsignal_computed.any()))

    # @unittest.skip("reason for skipping")
    def test_compute_a_from_Uin_Uquest_300_jens(self):
        Uquest_300 = genfromtxt(fixPath + 'data/test_data/Uquest_300_jens.csv', delimiter=',')
        Uin = genfromtxt(fixPath + 'data/test_data/Uin_jens.csv', delimiter=',')
        a_300_ideal = genfromtxt(fixPath + 'data/test_data/a_300_jens.csv', delimiter=',')

        Uin_mV = signalHelper.setVpp(signal=Uin, Vpp=300)
        Uquest_300_mV = signalHelper.convert_V_to_mV(Uquest_300)

        a_300_computed = compute_a_from_Uin_Uquet(Uin=Uin_mV, Uquest=Uquest_300_mV, N=3)

        err = linalg.norm(a_300_computed - a_300_ideal) / linalg.norm(a_300_ideal)
        self.assertTrue(err < 1e-3)

    def test_compute_a_from_Uin_Uquest_300_our(self):
        Uquest_300 = genfromtxt(fixPath + 'data/test_data/Uquest_300_our.csv', delimiter=',')
        Uin = genfromtxt(fixPath + 'data/test_data/Uin_our.csv', delimiter=',')
        a_300_ideal = genfromtxt(fixPath + 'data/test_data/a_300_our.csv', delimiter=',')

        Uin_mV = signalHelper.setVpp(signal=Uin, Vpp=300)
        Uquest_300_mV = signalHelper.convert_V_to_mV(Uquest_300)

        a_300_computed = compute_a_from_Uin_Uquet(Uin=Uin_mV, Uquest=Uquest_300_mV, N=3)

        err = linalg.norm(a_300_computed - a_300_ideal) / linalg.norm(a_300_ideal)
        self.assertTrue(err < 1e-3)

    def test_compute_K_from_a_jens(self):
        K_300_ideal = genfromtxt(fixPath + 'data/test_data/K_300_jens.csv', delimiter=',')

        a_300 = genfromtxt(fixPath + 'data/test_data/a_300_jens.csv', delimiter=',')

        K_computed = compute_K_from_a(a_300, verbosity=False)

        err = linalg.norm(K_computed - K_300_ideal) / linalg.norm(K_300_ideal)
        self.assertTrue(err < 1e-3)

    def test_compute_K_from_a_our(self):
        K_300_ideal = genfromtxt(fixPath + 'data/test_data/K_300_our.csv', delimiter=',')

        a_300 = genfromtxt(fixPath + 'data/test_data/a_300_our.csv', delimiter=',')

        K_computed = compute_K_from_a(a_300, verbosity=False)

        err = linalg.norm(K_computed - K_300_ideal) / linalg.norm(K_300_ideal)
        self.assertTrue(err < 1e-3)

    # @unittest.skip("reason for skipping")
    def test_compute_Uin_from_Uquest_jens(self):
        Uin_ideal = genfromtxt(fixPath + 'data/test_data/Uin_jens.csv', delimiter=',')
        Uin_mV_ideal = signalHelper.setVpp(signal=Uin_ideal, Vpp=300)
        Uquest_300 = genfromtxt(fixPath + 'data/test_data/Uquest_300_jens.csv', delimiter=',')
        Uquest_300_mV = signalHelper.convert_V_to_mV(Uquest_300)
        K_300 = genfromtxt(fixPath + 'data/test_data/K_300_jens.csv', delimiter=',')

        Uin_mV_computed = compute_Uin_from_Uquest(Uquest_300_mV, K_300, verbosity=False)

        _, Uin_mV_computed_overlay = overlay.overlay(Uin_mV_computed, Uin_mV_ideal)

        err = linalg.norm(Uin_mV_computed_overlay[:, 1] - Uin_mV_ideal[:, 1]) / linalg.norm(Uin_mV_ideal[:, 1])
        self.assertTrue(err < 0.2)

    def test_compute_Uin_from_Uquest_our(self):
        Uin_ideal = genfromtxt(fixPath + 'data/test_data/Uin_our.csv', delimiter=',')
        Uin_mV_ideal = signalHelper.setVpp(signal=Uin_ideal, Vpp=300)
        Uquest_300 = genfromtxt(fixPath + 'data/test_data/Uquest_300_our.csv', delimiter=',')
        Uquest_300_mV = signalHelper.convert_V_to_mV(Uquest_300)
        K_300 = genfromtxt(fixPath + 'data/test_data/K_300_our.csv', delimiter=',')

        Uin_mV_computed = compute_Uin_from_Uquest(Uquest_300_mV, K_300, verbosity=False)

        _, Uin_mV_computed_overlay = overlay.overlay(Uin_mV_computed, Uin_mV_ideal)



        err = linalg.norm(Uin_mV_computed_overlay[:, 1] - Uin_mV_ideal[:, 1]) / linalg.norm(Uin_mV_ideal[:, 1])
        self.assertTrue(err < 0.2)

    def test_setSampleRate(self):

        Uin = genfromtxt(fixPath + 'data/test_data/Uin_jens.csv', delimiter=',')

        sampleRate = 1e9

        T = max(Uin[:, 0]) - min(Uin[:, 0])
        lenght_new = int(np.floor(T * sampleRate))

        Uin_computed = signalHelper.setSampleRate(Uin, sampleRate);

        self.assertTrue(Uin_computed.shape[0] == lenght_new)

    def test_adjust_H_a_trivial(self):

        Halt = read_in_transfer_function(fixPath + 'data/test_data/H_jens.csv')

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

        Halt = read_in_transfer_function(fixPath + 'data/test_data/H_jens.csv')
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

        Halt = read_in_transfer_function(fixPath + 'data/test_data/H_jens.csv')
        Hneu_ideal = transfer_function(Halt.f)

        sigma_H = 0.5
        factor = 2
        Hneu_ideal.a = Halt.a * ( 1 + ( ( factor - 1 ) * sigma_H ) )
        Hneu_ideal.p = Halt.p
        #Tmax = 3e-6 # will not suceed: too little frequencies in spectrum of Uout_ideal
        Tmax = 3e-7 # will suceed: wide frequencie range in spectrum of Uout_ideal
        F_sample = 4*Halt.f[-1]
        N = int(np.ceil(Tmax*F_sample))
        print(N)
        t = np.linspace(0, Tmax, N)
        print('delta t' + str(t[1]-t[0]))
        # Do not change Signal because for above used formula signal has to contain every frequency possible
        Uout_ideal = generateSinSum(np.array([[1, 4 ],  [2, 6 ],  [3, 10 ]]), t)
        Uout_measured = np.zeros((Uout_ideal.shape[0], 2))
        Uout_measured[:, 0] = Uout_ideal[:, 0]
        Uout_measured[:,1] = [x*factor for x in Uout_ideal[:, 1]]

        Hneu = adjust_H(Halt, Uout_ideal, Uout_measured, sigma_H, verbosity=True)


        # this will never work: see plots, range of frequencies in signals is to low because of too little number of points
        err = linalg.norm(Hneu.c - Hneu_ideal.c) / linalg.norm(Hneu_ideal.c)

        self.assertTrue(err < 0.001) # we allow an error of 0.1% for the start, but it should be better

    def test_adjust_H (self):

        """
                if
                  Uout_ideal is a sum of three sin functions
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
        sampleRateAWG = 223 * f_rep
        f_BB = 5e6
        Vpp = 0.3
        Uout_ideal = np.transpose(
            generate_BBsignal(f_rep=f_rep, f_BB=f_BB, Vpp=Vpp, sampleRateAWG=sampleRateAWG, saveCSV=False, verbosity=0))
        Uout_measured = factor * Uout_ideal

        Halt = read_in_transfer_function_old(fixPath + 'data/adjustH/Messung2/Ha_0.csv', fixPath + 'data/adjustH/Messung2/Hp_0.csv')
        Hneu_ideal = transfer_function(Halt.f)
        Hneu_ideal.a = Halt.a * (1 - sigma_H*(factor - 1))
        Hneu_ideal.p = Halt.p
        ## to show pictures of first step of adjust_H in real application
        #Uout_measured = genfromtxt(fixPath + 'data/adjustH/Messung2/Uout_1.csv', delimiter=',')

        Hneu = adjust_H(Halt, Uout_ideal, Uout_measured, sigma_H=sigma_H, verbosity=True)

        err = linalg.norm(Hneu.c - Hneu_ideal.c) / linalg.norm(Hneu_ideal.c)

        self.assertTrue(err < 0.1)  # we allow an error of 0.1% for the start, but it should be better


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
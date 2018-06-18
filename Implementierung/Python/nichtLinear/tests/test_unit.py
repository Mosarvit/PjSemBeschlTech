from unittest import TestCase
from numpy import genfromtxt
from scipy import linalg
from blocks import compute_Uquest_from_Uout, compute_K_from_a, compute_Uin_from_Uquest, compute_a_from_Uin_Uquet

from helpers import overlay, signalHelper
import numpy as np
import copy
import matplotlib.pyplot as plt

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

       Ha = genfromtxt(fixPath + 'data/test_data/H_a_jens.csv', delimiter=',')
       Hph = genfromtxt(fixPath + 'data/test_data/H_p_jens.csv', delimiter=',')
       H = np.zeros(((Ha.shape[0]),3))
       H[:, 0:2] = Ha
       H[:, 2] = Hph[:, 1]

       Uquest_300_computed = compute_Uquest_from_Uout.compute(Uout=Uout_300, H=H, verbosity=False)

       err = linalg.norm(Uquest_300_computed[:,1] - Uquest_300_ideal[:,1]) / linalg.norm( Uquest_300_ideal[:,1])
       self.assertTrue(err < 0.03)

    def test_compute_Uquest_from_Uout_300_our(self):
        Uout_300 = genfromtxt(fixPath + 'data/test_data/Uout_300_our.csv', delimiter=',')
        Uquest_300_ideal = genfromtxt(fixPath + 'data/test_data/Uquest_300_our.csv', delimiter=',')

        Ha = genfromtxt(fixPath + 'data/test_data/H_a_our.csv', delimiter=',')
        Hph = genfromtxt(fixPath + 'data/test_data/H_p_our.csv', delimiter=',')
        H = np.zeros(((Ha.shape[0]), 3))
        H[:, 0:2] = Ha
        H[:, 2] = Hph[:, 1]

        Uquest_300_computed = compute_Uquest_from_Uout.compute(Uout=Uout_300, H=H, verbosity=False)

        err = linalg.norm(Uquest_300_computed[:, 1] - Uquest_300_ideal[:, 1]) / linalg.norm(Uquest_300_ideal[:, 1])
        self.assertTrue(err < 0.03)

    def test_compute_Uquest_from_Uout_with_BBsignal_ideal(self):

        BBsignal_ideal = genfromtxt(fixPath + 'data/test_data/BBsignal_ideal.csv', delimiter=',')
        Uquest_from_BBsignal_ideal = genfromtxt(fixPath + 'data/test_data/Uquest_from_BBsignal_our.csv', delimiter=',')

        Ha = genfromtxt(fixPath + 'data/test_data/H_a_our.csv', delimiter=',')
        Hph = genfromtxt(fixPath + 'data/test_data/H_p_our.csv', delimiter=',')
        H = np.zeros(((Ha.shape[0]), 3))
        H[:, 0:2] = Ha
        H[:, 2] = Hph[:, 1]

        Uquest_from_BBsignal_computed = compute_Uquest_from_Uout.compute(Uout=BBsignal_ideal, H=H, verbosity=False)

        err = linalg.norm(Uquest_from_BBsignal_computed[:,1] - Uquest_from_BBsignal_ideal[:,1]) / linalg.norm(Uquest_from_BBsignal_ideal[:,1])
        self.assertTrue(err<0.04)

    # @unittest.skip("reason for skipping")
    def test_compute_Uquest_from_Uout_catch_imaginary(self):

        BBsignal_ideal = genfromtxt(fixPath + 'data/test_data/BBsignal_ideal.csv', delimiter=',')

        Ha = genfromtxt(fixPath + 'data/test_data/H_a_our.csv', delimiter=',')
        Hph = genfromtxt(fixPath + 'data/test_data/H_p_our.csv', delimiter=',')
        H = np.zeros(((Ha.shape[0]), 3))
        H[:, 0:2] = Ha
        H[:, 2] = Hph[:, 1]

        Uquest_from_BBsignal_computed = compute_Uquest_from_Uout.compute(Uout=BBsignal_ideal, H=H, verbosity=False)

        self.assertFalse(np.iscomplex(Uquest_from_BBsignal_computed.any()))

    # @unittest.skip("reason for skipping")
    def test_compute_a_from_Uin_Uquest_300_jens(self):
        Uquest_300 = genfromtxt(fixPath + 'data/test_data/Uquest_300_jens.csv', delimiter=',')
        Uin = genfromtxt(fixPath + 'data/test_data/Uin_jens.csv', delimiter=',')
        a_300_ideal = genfromtxt(fixPath + 'data/test_data/a_300_jens.csv', delimiter=',')

        Uin_mV = signalHelper.setVpp(signal=Uin, Vpp=300)
        Uquest_300_mV = signalHelper.convert_V_to_mV(Uquest_300)

        a_300_computed = compute_a_from_Uin_Uquet.compute(Uin=Uin_mV, Uquest=Uquest_300_mV, N=3, verbosity=False)

        err = linalg.norm(a_300_computed - a_300_ideal) / linalg.norm(a_300_ideal)
        self.assertTrue(err < 1e-3)

    def test_compute_a_from_Uin_Uquest_300_our(self):
        Uquest_300 = genfromtxt(fixPath + 'data/test_data/Uquest_300_our.csv', delimiter=',')
        Uin = genfromtxt(fixPath + 'data/test_data/Uin_our.csv', delimiter=',')
        a_300_ideal = genfromtxt(fixPath + 'data/test_data/a_300_our.csv', delimiter=',')

        Uin_mV = signalHelper.setVpp(signal=Uin, Vpp=300)
        Uquest_300_mV = signalHelper.convert_V_to_mV(Uquest_300)

        a_300_computed = compute_a_from_Uin_Uquet.compute(Uin=Uin_mV, Uquest=Uquest_300_mV, N=3, verbosity=False)

        err = linalg.norm(a_300_computed - a_300_ideal) / linalg.norm(a_300_ideal)
        self.assertTrue(err < 1e-3)

    def test_compute_K_from_a_jens(self):
        K_300_ideal = genfromtxt(fixPath + 'data/test_data/K_300_jens.csv', delimiter=',')

        a_300 = genfromtxt(fixPath + 'data/test_data/a_300_jens.csv', delimiter=',')

        K_computed = compute_K_from_a.compute(a_300, verbosity=False)

        err = linalg.norm(K_computed - K_300_ideal) / linalg.norm(K_300_ideal)
        self.assertTrue(err < 1e-3)

    def test_compute_K_from_a_our(self):
        K_300_ideal = genfromtxt(fixPath + 'data/test_data/K_300_our.csv', delimiter=',')

        a_300 = genfromtxt(fixPath + 'data/test_data/a_300_our.csv', delimiter=',')

        K_computed = compute_K_from_a.compute(a_300, verbosity=False)

        err = linalg.norm(K_computed - K_300_ideal) / linalg.norm(K_300_ideal)
        self.assertTrue(err < 1e-3)

    # @unittest.skip("reason for skipping")
    def test_compute_Uin_from_Uquest_jens(self):
        Uin_ideal = genfromtxt(fixPath + 'data/test_data/Uin_jens.csv', delimiter=',')
        Uin_mV_ideal = signalHelper.setVpp(signal=Uin_ideal, Vpp=300)
        Uquest_300 = genfromtxt(fixPath + 'data/test_data/Uquest_300_jens.csv', delimiter=',')
        Uquest_300_mV = signalHelper.convert_V_to_mV(Uquest_300)
        K_300 = genfromtxt(fixPath + 'data/test_data/K_300_jens.csv', delimiter=',')

        Uin_mV_computed = compute_Uin_from_Uquest.compute(Uquest_300_mV, K_300, verbosity=False)

        _, Uin_mV_computed_overlay = overlay.overlay(Uin_mV_computed, Uin_mV_ideal)

        err = linalg.norm(Uin_mV_computed_overlay[:, 1] - Uin_mV_ideal[:, 1]) / linalg.norm(Uin_mV_ideal[:, 1])
        self.assertTrue(err < 0.2)

    def test_compute_Uin_from_Uquest_our(self):
        Uin_ideal = genfromtxt(fixPath + 'data/test_data/Uin_our.csv', delimiter=',')
        Uin_mV_ideal = signalHelper.setVpp(signal=Uin_ideal, Vpp=300)
        Uquest_300 = genfromtxt(fixPath + 'data/test_data/Uquest_300_our.csv', delimiter=',')
        Uquest_300_mV = signalHelper.convert_V_to_mV(Uquest_300)
        K_300 = genfromtxt(fixPath + 'data/test_data/K_300_our.csv', delimiter=',')

        Uin_mV_computed = compute_Uin_from_Uquest.compute(Uquest_300_mV, K_300, verbosity=False)

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


from unittest import TestCase
from numpy import genfromtxt
from scipy import linalg
from blocks import compute_Uquest_from_Uout, compute_K_from_a, compute_Uin_from_Uquest, compute_a_from_Uin_Uquet

from helpers import overlay, signalHelper
import numpy as np
import copy


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
    def test_compute_Uin_from_Uquest(self):

        Uin_ideal = genfromtxt(fixPath + 'data/test_data/Uin_jens.csv', delimiter=',')
        Uquest_300_ideal = genfromtxt(fixPath + 'data/test_data/Uquest_300_jens.csv', delimiter=',' )
        K_param2_300_ideal = genfromtxt(fixPath + 'data/test_data/K_param2_300.csv', delimiter=',')
        # why has Uin_ideal more time steps than Uquest_ideal???
        #  - because they come from different places. Uin is the input of the AWG nad Uquest is computed form the measured Uout
        # Uin_computed has same number of time steps as Uquest_ideal
        #  - corrent, since it was computed from Uquest
        Uin_computed = compute_Uin_from_Uquest.compute(Uquest_300_ideal, K_param2_300_ideal, verbosity=False)

        # testing the test
        # compare different time-steps:
        # print("Time steps given in Uquest", len(Uquest_300_ideal[:, 0]))
        # print("Time steps computed in Uin", len(Uin_computed[:, 0]))
        # print("Time steps expected", len(Uin_ideal[:, 0]))
        # # in1 = copy.copy(Uin_computed)
        # in1[0:2] = Uin_computed[-2:]
        # in1[2:] = Uin_computed[0:-2]

        # in1 = copy.copy(Uin_computed)
        # in1[0:1] = Uin_computed[-1:]
        # in1[1:] = Uin_computed[0:-1]

        # end testing the test
        # output is to be evaluated at same time steps as Uin_ideal
        Uin_computed_overlay = copy.copy(Uin_ideal)
        # overlay of voltages
        Uin_computed_overlay[:, 1] = overlay.overlay(Uin_computed, Uin_ideal ) #see little changes in overlay!!!
        #print("Time steps computed in Uin after overlay", len(Uin_computed_overlay[:, 0]))

        # verbosity = True
        # if verbosity:
        #     plt.figure(1)
        #     plt.plot(Uin_ideal[:, 0], Uin_ideal[:, 1])
        #     # plt.figure(2)
        #     # plt.plot(Uin_computed[:, 0], Uin_computed[:, 1])
        #     plt.figure(3)
        #     plt.plot(Uin_computed_overlay[:, 0], Uin_computed_overlay[:, 1])
        #     # plt.figure(2)
        #     # plt.plot(Uquest_300_ideal[:, 0], Uquest_300_ideal[:, 1])
        #     # plt.title('Spannungssignale')
        #     # plt.ylabel('u in mV')
        #     # plt.legend('U_in', 'H^-1*U_out')
        #     plt.show()

        err = linalg.norm(Uin_computed_overlay - Uin_ideal) / linalg.norm(Uin_ideal)
        self.assertTrue(err < 0.2)

    def test_compute_Uin_from_Uquest_sample_rate(self):

        Uin_ideal = genfromtxt(fixPath + 'data/test_data/Uin.csv', delimiter=',')
        Uquest_300_ideal = genfromtxt(fixPath + 'data/test_data/Uquest_300.csv', delimiter=',')
        K_param2_300_ideal = genfromtxt(fixPath + 'data/test_data/K_param2_300.csv', delimiter=',')

        sampleRateAWG = 1e9

        T = max(Uquest_300_ideal[:, 0]) - min(Uquest_300_ideal[:, 0])
        lenght_new = int(np.floor(T * sampleRateAWG))

        Uin_computed = compute_Uin_from_Uquest.compute(Uquest_300_ideal, K_param2_300_ideal, sampleRateAWG, verbosity=False)

        self.assertTrue(Uin_computed.shape[0] == lenght_new)


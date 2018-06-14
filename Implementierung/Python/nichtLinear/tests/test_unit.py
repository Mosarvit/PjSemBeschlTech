from unittest import TestCase
from numpy import genfromtxt
from scipy import linalg
from compute import compute_K_from_a, compute_a_from_Uin_Uquet, compute_Uin_from_Uquest, compute_Uquest_from_Uout

from helpers import overlay
import numpy as np
import copy
import matplotlib.pyplot as plt

class test_unit(TestCase):

    global fixPath # fuer den Fall, dass er H.csv nicht finden kann
    fixPath = '../'
    # fixPath = ''

    def __init__(self, *args, **kwargs):
        super(test_unit, self).__init__(*args, **kwargs)
        self.getHFromCSV()

    def getHFromCSV(self):

        Ha = genfromtxt(fixPath + 'data/test_data/H_a.csv', delimiter=',')
        Hph = genfromtxt(fixPath + 'data/test_data/H_p.csv', delimiter=',')

        self.H = np.zeros(((Ha.shape[0]),3))
        self.H[:, 0:2] = Ha
        self.H[:, 2] = Hph[:, 1]

    def getComplexHFromCSV(self):
        str_H = np.genfromtxt(fixPath + 'data/test_data/H.csv', dtype=str, delimiter=',')
        self.H_ = np.zeros((len(str_H)), dtype=complex)
        self.freqA = np.zeros((len(str_H)))
        for k in range(0, len(str_H)):
            self.H_[k] = np.complex(str_H[k, 1].replace('i', 'j'))
            self.freqA[k] = float(str_H[k, 0])

    # @unittest.skip("reason for skipping")
    def test_compute_Uquest_from_Uout_Vpp300(self):
        Uout_300 = genfromtxt(fixPath + 'data/test_data/Uout_300.csv', delimiter=',')
        Uquest_300_ideal = genfromtxt(fixPath + 'data/test_data/Uquest_300.csv', delimiter=',')

        Uquest_300_computed = compute_Uquest_from_Uout.compute(Uout_300, self.H, verbosity=False)

        err = linalg.norm(Uquest_300_computed[:,1] - Uquest_300_ideal[:,1]) / linalg.norm( Uquest_300_ideal[:,1])
        self.assertTrue(err < 0.03)

    # @unittest.skip("reason for skipping")
    def test_compute_Uquest_from_Uout_with_BBsignal_ideal(self):

        BBsignal_ideal = genfromtxt(fixPath + 'data/test_data/BBsignal_ideal.csv', delimiter=',')
        Uquest_from_BBsignal_ideal = genfromtxt(fixPath + 'data/test_data/Uquest_from_BBsignal_ideal.csv', delimiter=',')

        Uquest_from_BBsignal_computed = compute_Uquest_from_Uout.compute(BBsignal_ideal, self.H, verbosity=False)

        err = linalg.norm(Uquest_from_BBsignal_computed[:,1] - Uquest_from_BBsignal_ideal[:,1]) / linalg.norm(Uquest_from_BBsignal_ideal[:,1])
        self.assertTrue(err<0.04)

    # @unittest.skip("reason for skipping")
    def test_compute_Uquest_from_Uout_catch_imaginary(self):

        BBsignal_ideal = genfromtxt(fixPath + 'data/test_data/BBsignal_ideal.csv', delimiter=',')
        Uquest_from_BBsignal_computed = compute_Uquest_from_Uout.compute(BBsignal_ideal, self.H, verbosity=False)

        self.assertFalse(np.iscomplex(Uquest_from_BBsignal_computed.any()))

    # @unittest.skip("reason for skipping")
    def test_compute_a_from_Uin_Uquet(self):
        Uquest_300_matlab = genfromtxt(fixPath + 'data/test_data/Uquest_300.csv', delimiter=',')[:,1]
        Uin = np.transpose(genfromtxt(fixPath + 'data/test_data/Uin.csv', delimiter=',')[:, 1])
        a_param2_300_matlab = genfromtxt(fixPath + 'data/test_data/a_param2_300.csv', delimiter=',')

        vpp = 300e-3
        N = 3
        Uin = (vpp) / (max(Uin) - min(Uin)) * Uin * 1000

        a = compute_a_from_Uin_Uquet.compute(Uin, Uquest_300_matlab, N, False)

        err = linalg.norm(a - a_param2_300_matlab) / linalg.norm(a_param2_300_matlab)
        self.assertTrue(err < 1e-3)

    # @unittest.skip("reason for skipping")
    def test_compute_K_from_a(self):
        a_ideal_300 = genfromtxt(fixPath + 'data/test_data/a_param2_300.csv', delimiter=',')
        K_ideal_300 = genfromtxt(fixPath + 'data/test_data/K_param2_300.csv', delimiter=',')

        K_computed = compute_K_from_a.compute(a_ideal_300, verbosity=False)

        err = linalg.norm(K_computed - K_ideal_300) / linalg.norm(K_ideal_300)
        self.assertTrue(err < 1e-3)

    # @unittest.skip("reason for skipping")
    def test_compute_Uin_from_Uquest(self):

        Uin_ideal = genfromtxt(fixPath + 'data/test_data/Uin.csv', delimiter=',')
        Uquest_300_ideal = genfromtxt(fixPath + 'data/test_data/Uquest_300.csv', delimiter=',' )
        K_param2_300_ideal = genfromtxt(fixPath + 'data/test_data/K_param2_300.csv', delimiter=',')
        # why has Uin_ideal more time steps than Uquest_ideal???
        #  - because they come from different places. Uin is the input of the AWG nad Uquest is computed form the measured Uout
        # Uin_computed has same number of time steps as Uquest_ideal
        #  - corrent, since it was computed from Uquest
        Uin_computed = compute_Uin_from_Uquest.compute(Uquest_300_ideal, K_param2_300_ideal, 1e9, verbosity=False)

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
        Uin_computed_overlay[:, 1] = overlay.overlay(Uin_computed[:, 1], Uin_ideal[:, 1] ) #see little changes in overlay!!!
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
        print(err)
        self.assertTrue(err < 0.2)

    def test_compute_Uin_from_Uquest_sample_rate(self):



        Uin_ideal = genfromtxt(fixPath + 'data/test_data/Uin.csv', delimiter=',')
        Uquest_300_ideal = genfromtxt(fixPath + 'data/test_data/Uquest_300.csv', delimiter=',')
        K_param2_300_ideal = genfromtxt(fixPath + 'data/test_data/K_param2_300.csv', delimiter=',')

        sampleRateAWG = 1e9

        T = max(Uquest_300_ideal[:, 0]) - min(Uquest_300_ideal[:, 0])
        lenght_new = int(np.floor(T * sampleRateAWG))

        Uin_computed = compute_Uin_from_Uquest.compute(Uquest_300_ideal, K_param2_300_ideal, 1e9, verbosity=False)

        self.assertTrue(Uin_computed.shape[0] == lenght_new)


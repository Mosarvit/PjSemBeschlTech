from unittest import TestCase
from numpy import genfromtxt
from scipy import linalg
from compute import compute_K_from_a, compute_a_from_Uin_Uquet, compute_Uin_from_Uquest, compute_Uquest_from_Uout

from helpers import overlay
import numpy as np
import copy

class test_unit(TestCase):

    global fixPath # fuer den Fall, dass er H.csv nicht finden kann
    fixPath = '../'
    # fixPath = ''

    def __init__(self, *args, **kwargs):
        super(test_unit, self).__init__(*args, **kwargs)
        self.getHFromCSV()

    def getHFromCSV(self):

        Ha = genfromtxt(fixPath + 'data/testdata/H_a.csv', delimiter=',')
        Hph = genfromtxt(fixPath + 'data/testdata/H_p.csv', delimiter=',')

        self.H = np.zeros(((Ha.shape[0]),3))
        self.H[:, 0:2] = Ha
        self.H[:, 2] = Hph[:, 1]

    def getComplexHFromCSV(self):
        str_H = np.genfromtxt(fixPath + 'data/testdata/H.csv', dtype=str, delimiter=',')
        self.H_ = np.zeros((len(str_H)), dtype=complex)
        self.freqA = np.zeros((len(str_H)))
        for k in range(0, len(str_H)):
            self.H_[k] = np.complex(str_H[k, 1].replace('i', 'j'))
            self.freqA[k] = float(str_H[k, 0])

    # @unittest.skip("reason for skipping")
    def test_compute_Uquest_from_Uout_300(self):
        Uout = genfromtxt(fixPath + 'data/testdata/Uout_300.csv', delimiter=',')[:, 1 ]
        Uquest_ideal = genfromtxt(fixPath + 'data/testdata/Uquest_300.csv', delimiter=',')[:,1]

        Uquest_computed = compute_Uquest_from_Uout.compute(Uout, self.H, verbosity=False)

        err = linalg.norm(Uquest_computed - Uquest_ideal) / linalg.norm(Uquest_ideal)
        self.assertTrue(err < 0.03)

    # @unittest.skip("reason for skipping")
    def test_compute_Uquest_from_Uout_400(self):

        Uout = genfromtxt(fixPath + 'data/testdata/Uout_400.csv', delimiter=',')[:, 1]
        Uquest_matlab = genfromtxt(fixPath + 'data/testdata/Uquest_400.csv', delimiter=',') [:,1]

        Uquest = compute_Uquest_from_Uout.compute(Uout, self.H, verbosity=False)

        err = linalg.norm(Uquest - Uquest_matlab) / linalg.norm(Uquest_matlab)
        self.assertTrue(err<0.03)

    # @unittest.skip("reason for skipping")
    def test_compute_a_from_Uin_Uquet(self):
        Uquest_300_matlab = genfromtxt(fixPath + 'data/testdata/Uquest_300.csv', delimiter=',')[:,1]
        Uin = np.transpose(genfromtxt(fixPath + 'data/testdata/Uin.csv', delimiter=',')[:, 1])
        a_param2_300_matlab = genfromtxt(fixPath + 'data/testdata/a_param2_300.csv', delimiter=',')

        vpp = 300e-3
        N = 3
        Uin = (vpp) / (max(Uin) - min(Uin)) * Uin * 1000

        a = compute_a_from_Uin_Uquet.compute(Uin, Uquest_300_matlab, N, False)

        err = linalg.norm(a - a_param2_300_matlab) / linalg.norm(a_param2_300_matlab)
        self.assertTrue(err < 1e-3)

    # @unittest.skip("reason for skipping")
    def test_compute_K_from_a(self):
        a_ideal_300 = genfromtxt(fixPath + 'data/testdata/a_param2_300.csv', delimiter=',')
        K_ideal_300 = genfromtxt(fixPath + 'data/testdata/K_param2_300.csv', delimiter=',')

        K_computed = compute_K_from_a.compute(a_ideal_300, verbosity=False)

        err = linalg.norm(K_computed - K_ideal_300) / linalg.norm(K_ideal_300)
        self.assertTrue(err < 1e-3)

    # @unittest.skip("reason for skipping")
    def test_compute_Uin_from_Uquest(self):

        Uin_ideal = genfromtxt(fixPath + 'data/testdata/Uin.csv', delimiter=',')[:,1]
        Uquest_300_ideal = genfromtxt(fixPath + 'data/testdata/Uquest_300.csv', delimiter=',')
        K_param2_300_ideal = genfromtxt(fixPath + 'data/testdata/K_param2_300.csv', delimiter=',')

        Uin_computed = compute_Uin_from_Uquest.compute(Uquest_300_ideal, K_param2_300_ideal, verbosity=False)

        # testing the test

        # in1 = copy.copy(Uin_computed)
        # in1[0:2] = Uin_computed[-2:]
        # in1[2:] = Uin_computed[0:-2]

        # in1 = copy.copy(Uin_computed)
        # in1[0:1] = Uin_computed[-1:]
        # in1[1:] = Uin_computed[0:-1]

        # end testing the test

        Uin_computed = overlay.overlay(Uin_computed, Uin_ideal )

        err = linalg.norm(Uin_computed - Uin_ideal) / linalg.norm(Uin_ideal)
        self.assertTrue(err < 1e-3)
        print(err)

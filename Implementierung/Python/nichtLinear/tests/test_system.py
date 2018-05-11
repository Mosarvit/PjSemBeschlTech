from unittest import TestCase
from numpy import genfromtxt
from scipy import linalg

from compute import compute_a_from_Uin_Uquet, compute_Uquest_from_Uout
import numpy as np


class TestComputeParam(TestCase):

    global fixPath # fuer den Fall, dass er H.csv nicht finden kann
    fixPath = '../'
    # fixPath = ''

    def __init__(self, *args, **kwargs):
        super(TestComputeParam, self).__init__(*args, **kwargs)
        self.getHFromCSV()

    # @unittest.skip("reason for skipping")
    def test_System(self):
        u_out = genfromtxt(fixPath + 'data/testdata/out_300.csv', delimiter=',')[:, 1]
        U_in = np.transpose(genfromtxt(fixPath + 'data/testdata/U_in.csv', delimiter=',')[:, 1])
        u_quest = compute_Uquest_from_Uout.compute(u_out, self.H, self.freqA, False)

        a_param2_300_matlab = genfromtxt(fixPath + 'data/testdata/a_param2_300.csv', delimiter=',')

        N = 3
        vpp = 300e-3

        [a, K] = compute_a_from_Uin_Uquet.compute(U_in, vpp, u_quest, N, False)

        err = linalg.norm(a - a_param2_300_matlab) / linalg.norm(a_param2_300_matlab)
        self.assertTrue(err < 1e-3)
        print(err)

    def getHFromCSV(self):
        str_H = np.genfromtxt(fixPath + 'data/testdata/H.csv', dtype=str, delimiter=',')
        self.H = np.zeros((len(str_H)), dtype=complex)
        self.freqA = np.zeros((len(str_H)))
        for k in range(0, len(str_H)):
            self.H[k] = np.complex(str_H[k, 1].replace('i', 'j'))
            self.freqA[k] = float(str_H[k, 0])
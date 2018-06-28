from unittest import TestCase
from numpy import genfromtxt
from scipy import linalg

from blocks import compute_Uquest_from_Uout, compute_a_from_Uin_Uquet
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
        Uout = genfromtxt(fixPath + 'data/test_data/Uout_300.csv', delimiter=',')[:, 1]
        Uin = np.transpose(genfromtxt(fixPath + 'data/test_data/Uin.csv', delimiter=',')[:, 1])
        Uquest = compute_Uquest_from_Uout.compute_Uquest_from_Uout(Uout, self.H, self.freqA, False)

        a_param2_300_matlab = genfromtxt(fixPath + 'data/test_data/a_param2_300.csv', delimiter=',')

        N = 3
        vpp = 300e-3

        [a, K] = compute_a_from_Uin_Uquet.compute_a_from_Uin_Uquet(Uin, vpp, Uquest, N)

        err = linalg.norm(a - a_param2_300_matlab) / linalg.norm(a_param2_300_matlab)
        self.assertTrue(err < 1e-3)
        print(err)

    def getHFromCSV(self):
        str_H = np.genfromtxt(fixPath + 'data/test_data/H.csv', dtype=str, delimiter=',')
        self.H = np.zeros((len(str_H)), dtype=complex)
        self.freqA = np.zeros((len(str_H)))
        for k in range(0, len(str_H)):
            self.H[k] = np.complex(str_H[k, 1].replace('i', 'j'))
            self.freqA[k] = float(str_H[k, 0])
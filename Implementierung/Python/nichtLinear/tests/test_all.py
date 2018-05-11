import unittest
from unittest import TestCase
from numpy import genfromtxt
from scipy import linalg

import computea
import numpy as np

import computeU_out_to_U_quest


class TestComputeParam(TestCase):

    def __init__(self, *args, **kwargs):
        super(TestComputeParam, self).__init__(*args, **kwargs)
        self.getHFromCSV()

    # @unittest.skip("reason for skipping")
    def test_computeU_quest_300(self):
        u_out = genfromtxt('data/out_300.csv', delimiter=',')[:, 1 ]
        u_quest_ideal = genfromtxt('data/testdata/u_quest_300.csv', delimiter=',')

        u_quest = computeU_out_to_U_quest.compute(u_out, self.H, self.freqA, False)

        err = linalg.norm(u_quest - u_quest_ideal) / linalg.norm(u_quest_ideal)
        self.assertTrue(err < 1e-3)

    # @unittest.skip("reason for skipping")
    def test_computeU_quest_400(self):

        u_out = genfromtxt('data/out_400.csv', delimiter=',')[:, 1]
        u_quest_matlab = genfromtxt('data/testdata/u_quest_400.csv', delimiter=',')

        u_quest = computeU_out_to_U_quest.compute(u_out, self.H, self.freqA, False)

        err = linalg.norm(u_quest - u_quest_matlab) / linalg.norm(u_quest_matlab)
        self.assertTrue(err<1e-3)

    def test_computea(self):
        u_quest_300_matlab = genfromtxt('data/testdata/u_quest_300.csv', delimiter=',')
        U_in = np.transpose(genfromtxt('data/testdata/U_in.csv', delimiter=',')[:, 1])
        a_param2_300_matlab = genfromtxt('data/testdata/a_param2_300.csv', delimiter=',')

        vpp = 300e-3
        N = 3

        [a, K] = computea.compute(U_in, vpp, u_quest_300_matlab, N, False)

        err = linalg.norm(a - a_param2_300_matlab) / linalg.norm(a_param2_300_matlab)
        self.assertTrue(err < 1e-3)
        print(err)

    # @unittest.skip("reason for skipping")
    def test_System(self):
        u_out = genfromtxt('data/testdata/out_300.csv', delimiter=',')[:, 1]
        U_in = np.transpose(genfromtxt('data/testdata/U_in.csv', delimiter=',')[:, 1])
        u_quest = computeU_out_to_U_quest.compute(u_out, self.H, self.freqA, False)

        a_param2_300_matlab = genfromtxt('data/testdata/a_param2_300.csv', delimiter=',')

        N = 3
        vpp = 300e-3

        [a, K] = computea.compute(U_in, vpp, u_quest, N, False)

        err = linalg.norm(a - a_param2_300_matlab) / linalg.norm(a_param2_300_matlab)
        self.assertTrue(err < 1e-3)
        print(err)

    def getHFromCSV(self):
        str_H = np.genfromtxt('data/testdata/H.csv', dtype=str, delimiter=',')
        self.H = np.zeros((len(str_H)), dtype=complex)
        self.freqA = np.zeros((len(str_H)))
        for k in range(0, len(str_H)):
            self.H[k] = np.complex(str_H[k, 1].replace('i', 'j'))
            self.freqA[k] = float(str_H[k, 0])
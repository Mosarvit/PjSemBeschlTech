import unittest
from unittest import TestCase
import U_inp_allg
import Param_Signal as param
from numpy import genfromtxt
from numpy import linalg
import numpy as np


class TestU_inp_allg(TestCase):

    # def __init__(self, *args, **kwargs):
    #     super(TestU_inp_allg, self).__init__(*args, **kwargs)
    #     str_H = np.genfromtxt('testdata/H.csv', dtype=str, delimiter=',')
    #     self.H = np.zeros((len(str_H)), dtype=complex)
    #     self.freqA = np.zeros((len(str_H)))
    #     for k in range(0, len(str_H)):
    #         self.H[k] = np.complex(str_H[k, 1].replace('i', 'j'))
    #         self.freqA[k] = float(str_H[k, 0])

    @unittest.skip
    def test_U_inp_allg_400(self):

        u_out = genfromtxt('testdata/out_300.csv', delimiter=',')[:, 1]
        u_quest_matlab = genfromtxt('testdata/u_quest_300.csv', delimiter=',')

        u_quest = U_inp_allg.U_inp_allg(u_out, self.H, self.freqA, False)

        err = linalg.norm(u_quest - u_quest_matlab) / linalg.norm(u_quest_matlab)

        self.assertTrue(err<1e-3)

    @unittest.skip
    def test_U_inp_allg_400(self):

        u_out = genfromtxt('testdata/out_400.csv', delimiter=',')[:, 1]
        u_quest_matlab = genfromtxt('testdata/u_quest_400.csv', delimiter=',')

        u_quest = U_inp_allg.U_inp_allg(u_out, self.H, self.freqA, False)

        err = linalg.norm(u_quest - u_quest_matlab) / linalg.norm(u_quest_matlab)

        self.assertTrue(err<1e-3)

    @unittest.skip
    def test_computeParam(self):
        u_quest_300_matlab = genfromtxt('testdata/u_quest_300.csv', delimiter=',')
        U_in = np.transpose(genfromtxt('testdata/U_in.csv', delimiter=',')[:, 1])
        a_param2_300_matlab = genfromtxt('testdata/a_param2_300.csv', delimiter=',')

        vpp = 300e-3
        N = 3

        [a, K] = param.computeParam(U_in, vpp, u_quest_300_matlab, N, False)

        err = linalg.norm(a - a_param2_300_matlab) / linalg.norm(a_param2_300_matlab)
        self.assertTrue(err < 1e-3)
        print(err)

    @unittest.skip
    def test_All(self):

        u_out = genfromtxt('testdata/out_300.csv', delimiter=',')[:, 1]
        U_in = np.transpose(genfromtxt('testdata/U_in.csv', delimiter=',')[:, 1])
        u_quest = U_inp_allg.U_inp_allg(u_out, self.H, self.freqA, False)

        a_param2_300_matlab = genfromtxt('testdata/a_param2_300.csv', delimiter=',')

        N = 3
        vpp = 300e-3

        [a, K] = param.computeParam(U_in, vpp, u_quest, N, False)

        err = linalg.norm(a - a_param2_300_matlab) / linalg.norm(a_param2_300_matlab)
        self.assertTrue(err < 1e-3)
        print(err)



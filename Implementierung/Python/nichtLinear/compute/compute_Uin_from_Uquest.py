# -*- coding: utf-8 -*-
from numpy import genfromtxt


def compute(Uquest, K, amplitude, verbosity):

    global fixPath  # fuer den Fall, dass er H.csv nicht finden kann
    fixPath = '../'
    # fixPath = ''

    Uin_300 = genfromtxt(fixPath + 'data/testdata/Uin.csv', delimiter=',')[:, 1]

    return (Uin_300)
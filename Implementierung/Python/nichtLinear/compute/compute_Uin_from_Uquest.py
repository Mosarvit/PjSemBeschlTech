# -*- coding: utf-8 -*-
from numpy import genfromtxt
import numpy as np


def compute(Uquest, K, verbosity):

    # dummy value, damit der unit test kompeliert:
    Uin = np.zeros(len(Uquest))

    # # ideal output, damit der unit test bestanden wird:
    #
    # global fixPath    # wenn er Uin.csv nicht finden kann
    # fixPath = '../'   # entweder dies
    # # fixPath = ''    # oder das waehlen
    # Uin = genfromtxt(fixPath + 'data/testdata/Uin.csv', delimiter=',')[:, 1]

    return (Uin)
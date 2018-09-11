# -*- coding: utf-8 -*-
import numpy as np
#import FFT
from helpers.overlay import overlay
#import csv
#import os
#import time
#import FFT
#from scipy import interpolate
#import csv

def compute_a_from_Uin_Uquest(Uin, Uquest, N):

    """
    compute_a_from_Uin_Uquest calculates coefficients a from given U_in and U_quest

    INPUT:

        Uquest - instance of signal class

        Uin - input voltage to use, instance of signal class

        N - positive integer; polynomial degree

    OUTPUT:

        lsg - Nx1 vector; coefficients

    """

    l_out = len(Uquest.in_mV)

    # np.sin(Uin)
    Uin = overlay(Uin, Uquest)

    Uin = Uin.in_mV
    Uquest = Uquest.in_mV

    #normalization: u_out wird in V gemessen--> mV
    #u_in Normierung händisch anhand in_pp
                                             #STIMMT DAS IMMER?
    # Uin = (Uin_pp) / (max(Uin) - min(Uin)) * Uin * 1000



    # voltage matrix for linear equation system
    U = np.zeros((l_out, N))
    for ind in range(1, N+1):
        U[:, (ind-1)] = [np.power(x, ind) for x in Uin]

    a = np.linalg.lstsq(U, np.transpose(Uquest), rcond=-1)
    lsg = a[0]

    return (lsg)

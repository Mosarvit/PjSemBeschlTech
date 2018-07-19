# -*- coding: utf-8 -*-
import numpy as np
from helpers import overlay

def adjust_a(a_old, Uin, Uquest_ideal, Uquest_measured, sigma_a):
    """
    adjust_a optimize the coefficient a

    INPUT:

        a_old - Nx1 vector; coefficients; (N - polynomial degree of the curve)

       

    OUTPUT:

        a_new - Nx1 vector; coefficients; (N - polynomial degree of the curve)

    """

    Uquest_measured = overlay.overlay(Uquest_measured, Uquest_ideal)


    Uquest_ideal_vektor_mV = Uquest_ideal.in_mV
    Uquest_measured_vektor_mV = Uquest_measured.in_mV
    Uin_vektor_mV = Uin.in_mV
    l_out = len(Uquest_measured_vektor_mV)
    N = len(a_old)

    # voltage matrix
    U = np.zeros((l_out, N))
    delta = Uquest_measured_vektor_mV - Uquest_ideal_vektor_mV
    for ind in range(1, N + 1):
        U[:, (ind - 1)] = [np.power(x, ind) for x in Uin_vektor_mV]

    lsg = np.linalg.lstsq(U, np.transpose(delta), rcond=-1)
    a_delta = lsg[0]
    print(a_old)
    print(a_delta)
    a_new = a_old + sigma_a * a_delta
    return(a_new)
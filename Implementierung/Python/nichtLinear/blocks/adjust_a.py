# -*- coding: utf-8 -*-
import numpy as np

def adjust_a(a_old, Uin, Uquest_ideal, Uquest_measured, sigma_a):
    """
    adjust_a optimize the coefficient a

    INPUT:

        a_old - Nx1 vector; coefficients; (N - polynomial degree of the curve)

        Uquest_ideal - nx2 array; U_? (n - signal length)
            Uquest_ideal[:,0] - time vector
            Uquest_ideal[:,1] - signal vector

        Uquest_measured - nx2 array; (n - signal length)
            Uquest_measured[:,0] - time vector
            Uquest_measured[:,1] - signal vector

        sigma_a - scalar; increment

    OUTPUT:

        a_new - Nx1 vector; coefficients; (N - polynomial degree of the curve)

    """

    # Uin = Uin[:, 1]
    Uquest_ideal = Uquest_ideal[:, 1]
    Uquest_measured = Uquest_measured[:, 1]
    l_out = len(Uquest_measured)
    N = len(a_old)

    # voltage matrix
    U = np.zeros((l_out, N))
    delta = Uquest_measured - Uquest_ideal
    for ind in range(1, N + 1):
        U[:, (ind - 1)] = [np.power(x, ind) for x in Uin]

    lsg = np.linalg.lstsq(U, np.transpose(delta), rcond=-1)
    a_delta = lsg[0]

    a_new = a_old + sigma_a * a_delta
    return(a_new)
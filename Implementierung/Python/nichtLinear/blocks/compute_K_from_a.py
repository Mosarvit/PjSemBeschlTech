# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 12:09:14 2017

@author: denys
"""
import matplotlib.pyplot as plt
import numpy as np
from scipy.signal import argrelextrema
import settings


def compute_K_from_a(a, verbosity=0):
    """
    compute_K_a berechten die Lookup-Tabelle K aus den Vorfaktoren a

    INPUT:

        a - Nx1 vektor; die Vorfaktoren; (N - Polynomgrad der Approximierugnsmatrix)
        verbosity - boolean, ob Uin gelplottet werden soll

    OUTPUT:

        K - nx2 array; Lookuptabelle (n - Anzahl der Werte der Lookuptabelle)
            K[:,0] - Werte von Uin
            K[:,1] - Werte von Uquest

    """


    b = a;
    du = 1;

    M1=round(400/du)
    M=int(M1*2+1)
    K=np.zeros((M,2))
    L=len(b) 
    
    for i in range (0,M):
        K[i,0]=-M1+(i)*du
        for ind in range (0,L):
            K[i,1]=K[i,1]+b[ind]*K[i,0]**(ind+1)

    # #TODO ab hier Anpassung an bijektiven Teil
    bijectiv = True
    # nur für plots
    K_old = K
    if bijectiv:
        # initial index for maximum and minimum
        imin = 0
        imax = K.shape[0]
        # find index of local maximum and minimum
        k = np.where(K[:,0]==0)[0][0]
        for i in range(k,1,-1):
            if K[i, 1] < K[i - 1, 1] and K[i, 1] < K[i + 1, 1]:
                imin = i
        for i in range(k,K.shape[0]-1):
            if K[i, 1] > K[i - 1, 1] and K[i, 1] > K[i + 1, 1]:
                imax = i

        # for i in range(1,K.shape[0]-1):
        #     if K[i,1] > K[i-1,1] and K[i,1] > K[i+1,1]:
        #         imax = i
        #     elif K[i,1] < K[i-1,1] and K[i,1] < K[i+1,1]:
        #         imin = i


        # limit K to its bijectiv part
        # exclusive or inclusive?
        K = K[imin:imax, :]

    if verbosity:
        fig = plt.figure()
        plt.plot(K[:,0],K[:,1])
        plt.title('Kennlinie K')
        plt.xlabel('U_in in mV')
        plt.ylabel('U_out in mV')
        if settings.show_plots :
            plt.show()
        #fig.savefig('../../../ErstellteDokumente/Zwischenpraesentation/slides/ResultCode/plots/K.pdf')

        plt.figure()
        plt.subplot(1, 2, 1)
        plt.plot(K_old[:, 0], K_old[:, 1])
        plt.title('K vor bijektiver Anpassung')
        plt.xlabel('Uin')
        plt.ylabel('Uquest')

        plt.subplot(1, 2, 2)
        plt.plot(K[:, 0], K[:, 1])
        plt.title('K nach bijektiver Anpassung')
        plt.xlabel('Uin')
        plt.ylabel('Uquest')
        plt.show()
    
    return(K)




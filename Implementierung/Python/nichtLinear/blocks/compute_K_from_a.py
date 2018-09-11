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
    compute_K_a calculates the lookup-table K using the parameters a.
    The output will be the polynom in its bijective range around zero

    INPUT:

        a - Nx1 vector; parameters of the polynom; (N - polynomial grade of approximation-matrix)
        verbosity - boolean, whether Uin will be plotted

    OUTPUT:

        K - nx2 array; lookup-table in the bijectiv range, (n - number of values in table)
            K[:,0] - Uin in mV
            K[:,1] - Uquest in mV

    """


    b = a;
    du = 1;

    M1=round(300/du)
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
        # TODO: exclusive or inclusive?
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

#        plt.figure()
#        plt.subplot(1, 2, 1)
#        plt.plot(K_old[:, 0], K_old[:, 1])
#        plt.title('K vor bijektiver Anpassung')
#        plt.xlabel('Uin')
#        plt.ylabel('Uquest')

#        plt.subplot(1, 2, 2)
#        plt.plot(K[:, 0], K[:, 1])
#        plt.title('K in mV')
#        plt.xlabel('Uin')
#        plt.ylabel('Uquest')
#        plt.show()
    
    return(K)




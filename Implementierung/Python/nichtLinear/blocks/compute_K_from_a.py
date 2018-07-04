# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 12:09:14 2017

@author: denys
"""
import matplotlib.pyplot as plt
import numpy as np
import global_data


def compute_K_from_a(a, verbosity):
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

    M1=round(300/du)
    M=int(M1*2+1)
    K=np.zeros((M,2))
    L=len(b) 
    
    for i in range (0,M):
        K[i,0]=-M1+(i)*du
        for ind in range (0,L):
            K[i,1]=K[i,1]+b[ind]*K[i,0]**(ind+1)
    

    if verbosity:
        fig = plt.figure()
        plt.plot(K[:,0],K[:,1])
        plt.title('Kennlinie K')
        plt.xlabel('U_in in mV')
        plt.ylabel('U_out in mV')
        if global_data.showPlots :
            plt.show()
        #fig.savefig('../../../ErstellteDokumente/Zwischenpraesentation/slides/ResultCode/plots/K.pdf')
    
    return(K)




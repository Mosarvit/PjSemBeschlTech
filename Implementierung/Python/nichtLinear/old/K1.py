# -*- coding: utf-8 -*-
"""
Created on Wed Aug 23 12:09:14 2017

@author: denys
"""
def K1( b, du ):
        

    import numpy as np
    
    
    M1=round(300/du)
    M=M1*2+1
    K=np.zeros((M,2))
    L=len(b) 
    
    for i in range (0,M):
        K[i,0]=-M1+(i)*du
        for ind in range (0,L):
            K[i,1]=K[i,1]+b[ind]*K[i,0]**(ind+1)
    
    
    
    return(K)




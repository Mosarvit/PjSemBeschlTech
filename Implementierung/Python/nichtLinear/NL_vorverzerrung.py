# -*- coding: utf-8 -*-
"""
Created on Fri Nov 10 11:07:50 2017

@author: denys
"""
import numpy as np
from scipy.interpolate import interp1d
import math
import matplotlib.pyplot as plt
import time
import os
import csv
def NL_vorverzerrung( U, vpp, K ):
    
    directory = time.strftime("%d.%m.%Y_%H_%M_%S")
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.exists(directory + "/Plots"):
        os.makedirs(directory + "/Plots")
    if not os.path.exists(directory + "/csv"):
        os.makedirs(directory + "/csv")

    U[:,1]=U[:,1]*vpp/(max(U[:,1])-min(U[:,1]))
     

#%Steigung in linearem Bereich bestimmen
    N=np.size(K)
#%5% der Kennlinie für Fit der Steigung
    l=0.2
#%Runden
    n=round(N*l)
       
    ind1=np.where(K[:,1]>=0)
    ixc=ind1[0]
    ind1=math.floor(ixc[0])
    x=K[ind1:(ind1+n),0]   #%n Punkte von da an für die Linearisierungsgerade verwenden
    y=K[ind1:(ind1+n),1]
    m=(sum(y*x))/(sum(x*x)) #%Steigung
  
    if m*max(U[:,1])> max(K[:,1]):      #%Falls über die Kennlinie verzerrt würde: Linearisierungsgerade anpassen
            m=max(K[:,1])/max(U[:,1])
    

    if m*min(U[:,1])< min(K[:,1]):       #%auch im negativen Bereich
            m=min(K[:,1])/min(U[:,1])
    

#%Puffer
    m=m*0.999

    U_Steuer=np.linspace(round(min(K[:,0])),round(max(K[:,0])),(round(max(K[:,0]))-round(min(K[:,0])))*1000+1)
    f=interp1d(K[:,0], K[:,1])
    KL=f(U_Steuer)
    
    
    Kennlinie=np.column_stack((np.transpose(U_Steuer), np.transpose(KL)))
    U_vv=U
    print("Vorverzerren mit Kennlinie")
    for ind in range(0,np.size(U[:,0])):
        U_a=m*U[ind,1]   # ;%gewünschte Ausgangsspannung=Ui*m
        l=np.where(Kennlinie[:,1]>=U_a)     #;%in Kennlinie suchen -> Index l (Stelle, an der der Wert der Ausgangsspannung die gewünschte Spannung übersteigt)
        ls=l[0]
        l=ls[0]
        U_vv[ind,1]=Kennlinie[l,0]     #; %dem Zeitschritt die passende Steuerspannung zuordnen
    
    
    U_nl=U_vv
        
    plt.figure()
    plt.plot(U_nl[:,1])
    plt.grid(True)
    plt.ylabel('Unl')
    plt.show()
    
    with open(directory + '/csv/UinNL.csv', 'w', newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=';',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in range(0,U_nl[:,1].size):
            writer.writerow([str(U_nl[i,0]), str(U_nl[i,1])])
    
    with open(directory + '/csv/Kennlinie.csv', 'w', newline="") as csvfile:
        writer = csv.writer(csvfile, delimiter=';',
                        quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in range(0,K[:,0].size):
            writer.writerow([str(K[i,0]), str(K[i,1])])
    
    return (U_nl)
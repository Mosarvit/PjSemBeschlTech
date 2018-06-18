import numpy as np
import matplotlib.pyplot as plt
import csv
from helpers import csvHelper, globalVars

def generate(f_rep=900e3, f_BB=5e6, Vpp=3, samplerate2= 55556, saveCSV=True, verbosity=False):


    if samplerate2 % 2 == 1 :
        samplerate2 += 1

    T1 = 1 / f_BB
    T2 = 1 / f_rep
    samplerate1 = samplerate2/T2*T1

    if np.round(samplerate1)>samplerate1 :
        number = -1
    else :
        number = 1

    samplerate1rd = int(np.round(samplerate1))

    if samplerate1rd % 2 == 1 :
        samplerate1rd = samplerate1rd + number

    samplerate1 = samplerate1rd

    T1 = T2/samplerate2*samplerate1

    t1 = np.linspace(0, T1 , samplerate1+1)
    t2 = np.linspace(0, T2 , samplerate2+1)

    U1 = np.sin(2 * np.pi * f_BB * t1)

    U2 = np.zeros([2,samplerate2+1])
    U2[0,:] = t2;

    half1 = int(samplerate1/2)
    mid2 = int((samplerate2+1)/2)

    U2[1,mid2-half1:mid2+half1+1] = Vpp * U1

    if verbosity :
        fig = plt.figure()
        plt.plot(t2, U2[1,:])
        plt.title('Das ideale U_BB')
        plt.ylabel('u in mV')
        if globalVars.showPlots :
            plt.show()
        fig.savefig('../../../ErstellteDokumente/Zwischenpraesentation/slides/ResultCode/plots/Uout_ideal.pdf')

    if saveCSV :

        csvHelper.save_2cols('data/current_data/BBsignal_ideal.csv', U2[0,:], U2[1,:])

    return(U2)


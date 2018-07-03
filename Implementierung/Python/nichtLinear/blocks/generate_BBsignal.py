import numpy as np
import matplotlib.pyplot as plt
import csv
from helpers import csvHelper, globalVars

def generate_BBsignal(f_rep=900e3, f_BB=5e6, Vpp=3, sampleRateAWG=999900000, saveCSV=True, verbosity=False):

    """
    generate_BBsignal generiert ein ideales Barrie-Bucket-Signal nach den Vorgaben f_rep, f_BB, Vpp

    INPUT:

        f_rep - positive integer; Wiederhohlfrequenz
        f_BB - positive integer; Barrier-Bucket-Frequenz
        Vpp - positive integer; Spitze-zu-Spitze - Spannung
        samplerateAWG - positive integer; Abtastarte des AWG

        saveCSV - boolean; ob Uout gespreichert werden soll
        verbosity - boolean; ob Uin gelplottet werden soll

    OUTPUT:

        Uout - nx2 array; Barrie-Bucket-Signal
            Uout[:,0] - Zeitvektor
            Uout[:,1] - Signalvektor

    """

    numSamples = int(np.floor(sampleRateAWG / f_rep));

    if numSamples % 2 == 1 :
        numSamples += 1

    T1 = 1 / f_BB
    T2 = 1 / f_rep
    samplerate1 = numSamples / T2 * T1

    if np.round(samplerate1)>samplerate1 :
        number = -1
    else :
        number = 1

    samplerate1rd = int(np.round(samplerate1))

    if samplerate1rd % 2 == 1 :
        samplerate1rd = samplerate1rd + number

    samplerate1 = samplerate1rd

    T1 = T2 / numSamples * samplerate1

    t1 = np.linspace(0, T1 , samplerate1+1)
    t2 = np.linspace(0, T2, numSamples + 1)

    U1 = np.sin(2 * np.pi * f_BB * t1)

    Uout = np.zeros([2, numSamples + 1])
    Uout[0,:] = t2;

    half1 = int(samplerate1/2)
    mid2 = int((numSamples + 1) / 2)

    Uout[1,mid2-half1:mid2+half1+1] = Vpp * U1

    if verbosity :
        fig = plt.figure()
        plt.plot(t2, Uout[1,:])
        plt.title('Das ideale U_BB')
        plt.ylabel('u in mV')
        if globalVars.showPlots :
            plt.show()
#        fig.savefig('../../../ErstellteDokumente/Zwischenpraesentation/slides/ResultCode/plots/Uout_ideal.pdf')

    if saveCSV :

        csvHelper.save_2cols('data/current_data/BBsignal_ideal.csv', Uout[0,:], Uout[1,:])

    return(Uout)



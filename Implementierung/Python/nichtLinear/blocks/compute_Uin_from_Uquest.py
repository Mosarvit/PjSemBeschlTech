# -*- coding: utf-8 -*-
"""
Created on Sun June 3 2018
@author: Jonas
"""
import numpy as np
from scipy.interpolate import interp1d
import copy
import matplotlib.pyplot as plt
import settings
from helpers.find_nearest import find_nearest
from classes.signal_class import signal_class
from helpers.plot_helper import plot_2_signals



def compute_Uin_from_Uquest(Uquest, K, verbosity=False):

    """
    compute_Uin_from_Uquest berechten Uin aus Uquest mithilfe der Lookuptabelle K

    INPUT:

        Uquest - nx2 array; U_? (n - Länge des Signals)
            Uquest[:,0] - Zeitvektor
            Uquest[:,1] - Signalvektor

        K - nx2 array Lookuptabelle (n - Anzahl der Werte der Lookuptabelle)
            K[:,0] - Werte von Uin
            K[:,1] - Werte von Uquest

        verbosity - boolean, ob Uin gelplottet werden soll

    OUTPUT:

        Uin : nx2 array; (n - Länge des Signals)
            Uin[:,0] - Zeitvektor
            Uin[:,1] - Signalvektor

    """

    #VAS fuer Funktionalitaet ist Verhalten einer Potenzreihe in K -> keine Spruenge zw zwei Werten

    # dummy value, damit der unit test kompeliert:
    #Uin = np.zeros(len(Uquest))

    # # ideal output, damit der unit test bestanden wird:
    #
    # Comments von Beginn an implementiert
    # global fixPath    # wenn er Uin.csv nicht finden kann
    # fixPath = '../'   # entweder dies
    # # fixPath = ''    # oder das waehlen
    # Uin = genfromtxt(fixPath + 'data/mock_data/Uin.csv', delimiter=',')[:, 1]

    # Pseudo-Code in Comments:

    # Uquest i d Form (Time, Voltage) -> Uquest(:, 0) = Time, Uquest(:, 1) = Voltage [V]
    # K i d Form (Uin, Uquest) -> K(:, 0) = Uin Werte der Kennlinie in [mV], K(:, 1) = Uquest-Werte der Standard-Kennlinie in [mV]
    # Notwendig:



    # K = K / 1000 #Umrechnung in Volt

    #TODO der Teil hatte nicht das gemacht, was er sollte
    # - skaliere Kennlinie / Uebertragung bzw Ausgang fuer gewuenschte Amplitude max( norm(Uquest(:, 1)))
    # - pruefe auf Einhalten der Bijektivitaet durch Amplitude von Uquest,
    # uQuest_max = max(Uquest.in_mV)
    # uQuest_min = min(Uquest.in_mV)
    #
    # # - ggf. Anpassen des Ausgangsbereiches und Ausgeben einer Meldung
    # if uQuest_max > K[-1, 1]:
    #     uQuest_max_ind = find_nearest(Uquest.in_mV, uQuest_max)
    #     Uquest = signal_class( Uquest.time[0:uQuest_max_ind],  Uquest.in_mV [0:uQuest_max_ind] )
    #     print("Uquest adapted to range of K: max Uquest too high for bijectiv curve")
    # if uQuest_min < K[0, 1]:
    #     uQuest_min_ind = find_nearest(Uquest.in_mV, uQuest_min)
    #     Uquest = signal_class(Uquest.time[uQuest_min_ind:-1], Uquest.in_mV[uQuest_min_ind:-1])
    #     print("Uquest adapted to range of K: min Uquest too low for bijectiv curve")
    #setze Uin auf gleiche Groesse und gleiche Zeitwerte wie Uquest
    # Uin = copy.copy(Uquest)

    # indices for maximum and minimum initial
    imax = K.shape[0]
    imin = 0

    # find index of local maximum and minimum
    for i in range(1, K.shape[0] - 1):
        if K[i, 1] > K[i - 1, 1] and K[i, 1] > K[i + 1, 1]:
            imax = i
        elif K[i, 1] < K[i - 1, 1] and K[i, 1] < K[i + 1, 1]:
            imin = i

    # limit K to its bijectiv part
    # exclusive or inclusive?
    K_old = K
    K = K[imin:imax, :]

    # - interpoliere Kennlinie
    K_function = interp1d(K[:, 1], K[:, 0], kind='slinear')
    vpp_max = K[-1, 1] - K[0, 1]

    if verbosity:
        plt.figure()
        plt.subplot(2, 2, 1)
        plt.plot(Uquest.time, Uquest.in_mV)
        plt.title('vor Anpassung')
        plt.xlabel('t')
        plt.ylabel('Uquest')

    # adapt Uquest to max allowed vpp in mV
    if Uquest.Vpp*1000 > vpp_max*0.95:
        # der Wert 0.9 ist random gewählt, weil 1 nicht geklappt hat.. müssen wir herausfinden was geht
        Uquest.Vpp = 0.95*vpp_max/1000
        print('Uquest adapted to K maximum, new Vpp: ' + str(Uquest.Vpp))


    # - werte interpolierte Kennlinie an den gewunschten Werten Uquest(:, 1) aus
    Uin_in_mV = K_function(Uquest.in_mV)
    Uin = signal_class(Uquest.time, Uin_in_mV/1000)     #### woher der Faktor 10 vorher????

    if verbosity:
        plt.subplot(2, 2, 2)
        plt.plot(Uquest.time, Uquest.in_mV)
        plt.title('nach Anpassung')
        plt.xlabel('t')
        plt.ylabel('Uquest neu')

        plt.subplot(2, 2, 3)
        plt.plot(K_old[:, 0], K_old[:, 1])
        plt.title('K vor bijektiver Anpassung')
        plt.xlabel('Uin')
        plt.ylabel('Uquest')

        plt.subplot(2, 2, 4)
        plt.plot(K[:, 0], K[:, 1])
        plt.title('K nach bijektiver Anpassung')
        plt.xlabel('Uin')
        plt.ylabel('Uquest')
        plt.show()

    # - speichere Ausgang mit Uin(:, 1) = Uquest(:, 1) gleiche Zeitpunkte und interpolierten Werten

    if verbosity:
        fig = plt.figure()
        plt.plot(Uin.time,Uin.in_mV)
        plt.title('Uin')
        plt.ylabel('u')
        plt.ylabel('t')
        if settings.show_plots :
            plt.show()
        #fig.savefig('../../../ErstellteDokumente/Zwischenpraesentation/slides/ResultCode/plots/U_in.pdf')

    # Uin[:,1] = Uin[:,1];

    # Uin_obj = signal_class.gen_signal_from_old_convention(Uin)

    return (Uin)
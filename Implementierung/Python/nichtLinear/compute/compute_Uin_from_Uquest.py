# -*- coding: utf-8 -*-
"""
Created on Sun June 3 2018
@author: Jonas
"""
from numpy import genfromtxt
import numpy as np
from scipy.interpolate import interp1d
import copy
import matplotlib.pyplot as plt
from helpers import conform_to_sampleRateAWG


def compute(Uquest, K, sampleRateAWG, verbosity=False):
    #VAS fuer Funktionalitaet ist Verhalten einer Potenzreihe in K -> keine Spruenge zw zwei Werten

    # dummy value, damit der unit test kompeliert:
    #Uin = np.zeros(len(Uquest))

    # # ideal output, damit der unit test bestanden wird:
    #
    # Comments von Beginn an implementiert
    # global fixPath    # wenn er Uin.csv nicht finden kann
    # fixPath = '../'   # entweder dies
    # # fixPath = ''    # oder das waehlen
    # Uin = genfromtxt(fixPath + 'data/test_data/Uin.csv', delimiter=',')[:, 1]

    # Pseudo-Code in Comments:

    # Uquest i d Form (Time, Voltage) -> Uquest(:, 0) = Time, Uquest(:, 1) = Voltage [V]
    # K i d Form (Uin, Uquest) -> K(:, 0) = Uin Werte der Kennlinie in [mV], K(:, 1) = Uquest-Werte der Standard-Kennlinie in [mV]
    # Notwendig:

    # schraenke K auf surjektiven Bereich ein ---- ggf spaeter als helper auslagern!
    # erste Maxima und Minima fuer N != 3
    K_ind_high = int(np.argmax(K[:, 0]))
    K_ind_low = int(np.argmin(K[:, 0]))
    K = K[K_ind_low:K_ind_high, :]
    K = K / 1000 #Umrechnung in Volt

    # - skaliere Kennlinie / Uebertragung bzw Ausgang fuer gewuenschte Amplitude max( norm(Uquest(:, 1)))
    # - pruefe auf Einhalten der Bijektivitaet durch Amplitude von Uquest,
    uQuest_max = max(Uquest [:, 1])
    uQuest_min = min(Uquest[:, 1])

    # - ggf. Anpassen des Ausgangsbereiches und Ausgeben einer Meldung
    if uQuest_max > K[-1, 1]:
        uQuest_max_ind = Uquest[:, 1].find(uQuest_max)
        Uquest = Uquest [0:uQuest_max_ind, :]
        print("Uquest adapted to range of K: max Uquest too high for bijectiv curve")
    if uQuest_min < K[0, 1]:
        uQuest_min_ind = Uquest[:, 1].find(uQuest_min)
        Uquest = Uquest [uQuest_min_ind:-1, :]
        print("Uquest adapted to range of K: min Uquest too low for bijectiv curve")

    #setze Uin auf gleiche Groesse und gleiche Zeitwerte wie Uquest
    Uin = copy.copy(Uquest)

    # - interpoliere Kennlinie
    K_function = interp1d(K[:, 1], K[:, 0], kind='slinear')

    # - werte interpolierte Kennlinie an den gewunschten Werten Uquest(:, 1) aus
    Uin[:, 1] = K_function(Uquest[:, 1])/10     #### woher der Faktor 10 vorher????

    # passe die Lange von Uin an sampleRateAWG an

    Uin = conform_to_sampleRateAWG.conform(Uin=Uin, sampleRateAWG=999900000)

    # - speichere Ausgang mit Uin(:, 1) = Uquest(:, 1) gleiche Zeitpunkte und interpolierten Werten

    if verbosity:
        plt.figure()
        plt.plot(Uin[:,0],Uin[:,1])
        plt.title('Uin')
        plt.ylabel('u')
        plt.ylabel('t')
        plt.show()

    return (Uin)
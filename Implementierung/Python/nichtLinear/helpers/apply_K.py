# -*- coding: utf-8 -*-
"""
Created on Sun June 3 2018
@author: Jonas
"""
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import colorama

import settings
from classes.signal_class import signal_class
from helpers.K_helper import invert_K
import math


def apply_K(K_x_to_y, Ux, verbosity):

    # This is a crutch, to adjust the functionlality to new desing. todo: adjust the rest of the code to get rid of this line
    ###################################
    K_y_to_x = invert_K(K_x_to_y)
    ###################################

    # VAS fuer Funktionalitaet ist Verhalten einer Potenzreihe in K -> keine Spruenge zw zwei Werten
    # dummy value, damit der unit test kompeliert:
    # Uin = np.zeros(len(Uquest))
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
    # TODO der Teil hatte nicht das gemacht, was er sollte
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
    # setze Uin auf gleiche Groesse und gleiche Zeitwerte wie Uquest
    # Uin = copy.copy(Uquest)
    # indices for maximum and minimum initial
    imax = K_y_to_x.shape[0]
    imin = 0
    # find index of local maximum and minimum
    for i in range(1, K_y_to_x.shape[0] - 1):
        if K_y_to_x[i, 1] > K_y_to_x[i - 1, 1] and K_y_to_x[i, 1] > K_y_to_x[i + 1, 1]:
            imax = i
        elif K_y_to_x[i, 1] < K_y_to_x[i - 1, 1] and K_y_to_x[i, 1] < K_y_to_x[i + 1, 1]:
            imin = i
    # limit K to its bijectiv part
    # exclusive or inclusive?
    K_old = K_y_to_x
    K_y_to_x = K_y_to_x[imin:imax, :]
    # maximal zugelassene Werte für Uquest
    K_min_V = K_y_to_x[0, 1] / 1000
    K_max_V = K_y_to_x[-1, 1] / 1000
    Uquest_max_V = max(Ux.in_V)
    Uquest_min_V = min(Ux.in_V)
    vpp = Ux.Vpp
    # vpp_new = Uquest.Vpp
    vpp_new1 = vpp
    vpp_new2 = vpp
    # - interpoliere Kennlinie
    K_function = interp1d(K_x_to_y[:, 0], K_x_to_y[:, 1], kind='slinear')


    ###########
    K_functionV = interp1d(K_x_to_y[:, 0]/1000, K_x_to_y[:, 1]/1000, kind='slinear')
    #############

    K0 = K_x_to_y[:, 0]
    K1 = K_x_to_y[:, 1]

    # vpp_max = K[-1, 1] - K[0, 1]
    if verbosity:
        plt.figure()
        plt.subplot(2, 2, 1)
        plt.plot(Ux.time, Ux.in_mV)
        plt.title('vor Anpassung')
        plt.xlabel('t')
        plt.ylabel('Uquest')
    # adapt Uquest to max allowed vpp in mV
    # the task is to search für the biggest difference between the maximum of K and Uquest or minimum
    # if K_max_V - Uquest_max_V < 0:
    #     if K_min_V - Uquest_min_V > 0:
    #         if abs(K_max_V - Uquest_max_V) < abs(K_min_V - Uquest_min_V):
    #             vpp_new = abs(K_min_V/(Uquest_min_V/vpp))
    #         else:
    #             vpp_new = abs(K_max_V / (Uquest_max_V / vpp))
    #     else:
    #         vpp_new = abs(K_max_V / (Uquest_max_V / vpp))
    # elif K_min_V - Uquest_min_V > 0:
    #     vpp_new = abs(K_min_V / (Uquest_min_V / vpp))
    # Uquest.Vpp = vpp_new

    # Color for print()
    colorama.init()
    round_by = 15
    # berechnet unabhänig beide Vpp aus und setzt das kleinere
    if K_max_V - Uquest_max_V < 0:
        vpp_new1 = abs(K_max_V / (Uquest_max_V / vpp))
        vpp_new1 = math.floor(vpp_new1*10**round_by)/(10**round_by)
    if K_min_V - Uquest_min_V > 0:
        vpp_new2 = abs(K_min_V / (Uquest_min_V / vpp))
        vpp_new2 = math.floor(vpp_new2*10**round_by)/(10**round_by)
    if vpp_new1 < vpp_new2:
        Ux.Vpp = vpp_new1
        print(colorama.Back.RED + colorama.Style.BRIGHT + 'Warning: Uquest Vpp set to: '+ str(vpp_new1) + colorama.Style.NORMAL + colorama.Back.RESET)
    else:
        Ux.Vpp = vpp_new2
        print(colorama.Back.RED + colorama.Style.BRIGHT + 'Warning: Uquest Vpp set to: ' + str(vpp_new2) + colorama.Style.NORMAL + colorama.Back.RESET)
    # if Uquest.Vpp*1000 > vpp_max*0.95:
    #     # der Wert 0.9 ist random gewählt, weil 1 nicht geklappt hat.. müssen wir herausfinden was geht
    #     Uquest.Vpp = 0.95*vpp_max/1000
    #     print('Uquest adapted to K maximum, new Vpp: ' + str(Uquest.Vpp))
    # - werte interpolierte Kennlinie an den gewunschten Werten Uquest(:, 1) aus
    # Uy_in_mV = K_function(Ux.in_mV)
    # Uy = signal_class(Ux.time, Uy_in_mV / 1000)

    #######################
    Uy_in_V = K_functionV(Ux.in_V)
    Uy = signal_class(Ux.time, Uy_in_V )
    #######################


    if verbosity:
        plt.subplot(2, 2, 2)
        plt.plot(Ux.time, Ux.in_mV)
        plt.title('nach Anpassung')
        plt.xlabel('t')
        plt.ylabel('Uquest neu')

        plt.subplot(2, 2, 3)
        plt.plot(K_old[:, 0], K_old[:, 1])
        plt.title('K vor bijektiver Anpassung')
        plt.xlabel('Uin')
        plt.ylabel('Uquest')

        plt.subplot(2, 2, 4)
        plt.plot(K_y_to_x[:, 0], K_y_to_x[:, 1])
        plt.title('K nach bijektiver Anpassung')
        plt.xlabel('Uin')
        plt.ylabel('Uquest')
        if settings.show_plots:
            plt.show()
    # - speichere Ausgang mit Uin(:, 1) = Uquest(:, 1) gleiche Zeitpunkte und interpolierten Werten
    # Uin[:,1] = Uin[:,1];
    # Uin_obj = signal_class.gen_signal_from_old_convention(Uin)
    return Ux, Uy
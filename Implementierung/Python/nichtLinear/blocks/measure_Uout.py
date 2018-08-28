# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 11:22:44 2017

@author: denys
"""
from helpers.write_to_AWG import write_to_AWG
import numpy as np
import matplotlib.pyplot as plt
from helpers.csv_helper import save_2cols
from numpy import genfromtxt
from helpers.signal_helper import assemble_signal
from helpers.overlay import overlay
from helpers.read_from_DSO_resolution import read_from_DSO_resolution
from classes.signal_class import signal_class
from settings import show_plots, use_mock_system, mock_system, sample_rate_DSO, f_rep
from helpers.plot_helper import plot_2_signals
from helpers.csv_helper import save_signal

def measure_Uout(Uin, sample_rate_DSO=sample_rate_DSO, id='', loadCSV=0, saveCSV=0, verbosity=0):

    """
    compute_Uin_from_Uquest berechnet Uin aus Uquest mithilfe der Lookuptabelle K

    INPUT:

        Uin - n1x2 array; Eingangssignal in Volt :
            Uquest[:,0] - Zeitvektor
            Uquest[:,1] - Signalvektor

        sampleRateDSO - skalar; Abtastrate des DSO

        saveCSV - boolean; ob Uout gespreichert werden soll
        loadCSV - boolean; ob Uout aus vorhandenen CSV-Datei ausgelesen werden soll
        verbosity - boolean; ob Uout gelplottet werden soll

    OUTPUT:

        Uout_measured - n2x2 array; das gemessene Uout :
            Uout_measured[:,0] - Zeitvektor
            Uout_measured[:,1] - Signalvektor

        Uin_measured - n2x2 array; das gemessene Uin :
            Uin_measured[:,0] - Zeitvektor
            Uin_measured[:,1] - Signalvektor

    """

    ####################################################################################################################
    # Local functions
    ####################################################################################################################

    def send_Uin_to_AWG(Uin):
        if use_mock_system:
            mock_system.write_to_AWG(Uin.normalized, Uin.Vpp, frequency=f_rep)
        else:
            write_to_AWG(Uin.normalized, Uin.Vpp, frequency=f_rep)
        # TODO: change frequency-value to global-data (enable different repetition rate here)

    def receive_from_DSO(Uin):
        fmax = 80e6

        if use_mock_system:
            [time, dataUin, dataUout] = mock_system.read_from_DSO_resolution(sample_rate_DSO, Uin.Vpp, fmax, Uin.in_V)
        else:
            [time, dataUin, dataUout] = read_from_DSO_resolution(sample_rate_DSO, Uin.Vpp, fmax, Uin.in_V)

        Uout_measured = signal_class(time, dataUout)
        Uin_measured = signal_class(time, dataUin)

        return(Uin_measured, Uout_measured)

    ####################################################################################################################
    # Here the actual function begins.
    ####################################################################################################################

    if loadCSV :
        Uout_measured = genfromtxt('data/current_data/Uout_' +id+ '.csv', delimiter=',')
        Uin_measured = genfromtxt('data/current_data/Uin_' + id + '.csv', delimiter=',')
    else:
        send_Uin_to_AWG( Uin )
        Uin_measured, Uout_measured  = receive_from_DSO(Uin)

    if saveCSV:

        save_signal(signal=Uin_measured, filename='data/current_data/Uin_' + id + '.csv')
        save_signal(signal=Uout_measured, filename='data/current_data/Uout_' + id + '.csv')

    if verbosity:
        plot_2_signals(U1=Uin_measured, U2=Uout_measured, legend1='Uin_measured', legend2='Uout_measured')

    return(Uin_measured, Uout_measured)





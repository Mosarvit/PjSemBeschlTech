from blocks import get_H
import numpy as np
import matplotlib.pyplot as plt
from numpy import genfromtxt
from helpers import csv_helper
from classes.transfer_function_class import transfer_function_class
from global_data import use_mock_system, project_path, show_plots, mock_system
from helpers.csv_helper import read_in_transfer_function, read_in_transfer_function_old_convention, save_transfer_function
from helpers.plot_helper import plot_transfer_function

def measure_H(loadCSV=0, saveCSV=0, verbosity=0):

    """
    measure_H misst die Übertragungsfunktion

    INPUT:

        saveCSV - boolean; ob H gespreichert werden soll
        loadCSV - boolean; ob H aus vorhandenen CSV-Datei ausgelesen werden soll
        verbosity - boolean; ob H gelplottet werden soll

    OUTPUT:

        H - nx3 array; Übertragungsfunktion (old Version) :
            H[:,0] - Frequenz f
            H[:,1] - Amplitudenverstärkung
            H[:,2] - Phasenverschiebung

        Instance of transfer_funtion_class:
            Halt.f - Frequences f
            Halt.a - Amplitude a
            Halt.p - Phaseshift p
            Halt.c - Complex Value c = a*exp(jp)

    """

    if loadCSV :

        H = read_in_transfer_function('data/current_data/H.csv')

    else :

        if use_mock_system :

            H = mock_system.H

        else :

            fmax = 80e6
            vpp = 40e-3
            f, Ha, Hph = get_H.compute(fmax, vpp, bits=9)

            H = transfer_function_class(f)
            H.a = Ha
            H.p = Hph

            if saveCSV:
                save_transfer_function(H, 'data/current_data/H.csv')

    if verbosity:

        plot_transfer_function(H, 'H')

    return H
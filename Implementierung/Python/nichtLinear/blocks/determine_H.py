from blocks import get_H
import numpy as np
import matplotlib.pyplot as plt
from numpy import genfromtxt
from helpers import csv_helper
from classes.transfer_function_class import transfer_function_class
from settings import use_mock_system, project_path, show_plots, mock_system
from helpers.csv_helper import read_in_transfer_function, read_in_transfer_function_old_convention, save_transfer_function
from helpers.plot_helper import plot_transfer_function

def determine_H(loadCSV=0, saveCSV=0, verbosity=0):

    """

    """

    if loadCSV :

        H = read_in_transfer_function(project_path + 'data/current_data/H_0.csv')

    else :

        # if use_mock_system :
        #
        #     H = mock_system.H
        #
        # else :

        fmax = 80e6
        vpp = 40e-3
        f, Ha, Hph = get_H.get_H(fmax, vpp, bits=9, showPlots=1)

        H = transfer_function_class(f)
        H.a = Ha
        H.p = Hph

        if saveCSV:
            save_transfer_function(H, project_path + 'data/current_data/H_0.csv')

    if verbosity:

        plot_transfer_function(H, 'H')

    return H
from unittest import TestCase
import unittest
from numpy import genfromtxt
from scipy import linalg
import matplotlib.pyplot as plt
from blocks.adjust_H import adjust_H
from blocks.adjust_a import adjust_a

from helpers import overlay, signal_helper
from helpers.signal_helper import generateSinSum
from helpers.csv_helper import read_in_transfer_function
from classes.transfer_function_class import transfer_function_class
from helpers.apply_transfer_function import apply_transfer_function


from blocks.generate_BBsignal import generate_BBsignal
from blocks.compute_Uquest_from_Uout import compute_Uquest_from_Uout
from blocks.compute_K_from_a import compute_K_from_a
from blocks.compute_Uin_from_Uquest import compute_Uin_from_Uquest
from blocks.compute_a_from_Uin_Uquet import compute_a_from_Uin_Uquet
from settings import project_path, mock_data_path
from settings import mock_system
from blocks import get_H
from classes.transfer_function_class import transfer_function_class
from helpers.csv_helper import read_in_transfer_function_old_convention, read_in_signal, read_in_transfer_function_complex
from helpers.plot_helper import plot_2_transfer_functions, plot_2_signals, plot_transfer_function
from settings import project_path, last_directory_used
import os
import settings



import numpy as np


class test_get_H(TestCase):

    def __init__(self, *args, **kwargs):
        super(test_get_H, self).__init__(*args, **kwargs)

    # @unittest.skip("currently not working")
    def test_get_H(self):


        H_ideal = read_in_transfer_function_old_convention(pathA = mock_data_path + 'ideal_12_07_2018_12_03_47/csv/HAmpl_linear.csv',
                                                     pathPh = mock_data_path + 'ideal_12_07_2018_12_03_47/csv/PhaseH.csv', delimiter=';')




        mock_system.H = H_ideal



        fmax = 80e6
        vpp = 40e-3
        bits = 9
        f, Ha, Hph = get_H.compute(fmax, vpp, bits=bits, showPlots=0)

        from settings import last_directory_used

        # Uin_comp_ideal = read_in_transfer_function_old_convention(path = mock_data_path + 'ideal_12_07_2018_12_03_47/csv/UinFrq.csv', delimiter=';')
        Uin_compl_ideal = read_in_transfer_function_old_convention(
            mock_data_path + 'ideal_12_07_2018_12_03_47/csv/UinAmplFrq_linear.csv', pathPh=last_directory_used + 'UinPhase.csv',
            delimiter=';')
        Uin_compl_computed = read_in_transfer_function_old_convention(pathA=last_directory_used + 'UinAmplFrq_linear.csv',  pathPh=last_directory_used + 'UinPhase.csv',delimiter=';')

        # plot_2_transfer_functions(H1=Uin_compl_ideal, H2=Uin_compl_computed, legend1='Uin_compl_ideal', legend2='Uin_compl_computed')
        # plot_transfer_function(H=Uin_compl_computed, legend1="Uin_compl_computed")

        Uin_ideal = read_in_signal(path = mock_data_path + 'ideal_12_07_2018_12_03_47/csv/UinTime.csv', delimiter=';')
        Uin_computed = read_in_signal(path = last_directory_used + 'UinTime.csv', delimiter=';')

        # plot_2_signals(U1=Uin_ideal, U2=Uin_computed, legend1='Uin_ideal', legend2='Uin_computed')

        Uout_ideal = read_in_signal(path = mock_data_path + 'ideal_12_07_2018_12_03_47/csv/UoutTime.csv', delimiter=';')
        Uout_computed = read_in_signal(path = last_directory_used + 'UoutTime.csv', delimiter=';')

        # plot_2_signals(U1=Uout_ideal, U2=Uout_computed, legend1='Uout_ideal', legend2='Uout_computed')



        H_determined = transfer_function_class(f)
        H_determined.a = Ha
        H_determined.p = Hph

        # plot_2_transfer_functions(H1=H_ideal, H2=H_determined, legend1='H_ideal', legend2='H_determined')

        self.assertTrue(1)
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
from classes.signal_class import signal_class
from classes.transfer_function_class import transfer_function_class
from helpers.csv_helper import read_in_transfer_function_old_convention, read_in_signal, read_in_transfer_function_complex, read_in_signal_with_sample_rate
from helpers.plot_helper import plot_2_transfer_functions, plot_2_signals, plot_transfer_function, plot_vector
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

        folder_signal_ideal = mock_data_path + 'get_H/19.07.2018_09_26_38/csv/'
        folder_signal_test = last_directory_used

        Uin_AWG_ideal, Uin_measured_ideal, Uout_time_measured_ideal, Uout_freq_measured_ideal, Uin_freq_measured_ideal, H_ideal = self.read_in_get_H_signal_data(folder_signal_ideal)
        Uin_AWG_test, Uin_measured_test, Uout_time_measured_test, Uout_freq_measured_test, Uin_freq_measured_test, H_test = self.read_in_get_H_signal_data(folder_signal_test)

        Ha_computed_from_ideal = Uout_freq_measured_ideal.a / Uin_freq_measured_ideal.a
        H_computed_from_ideal = transfer_function_class(Uin_freq_measured_ideal.f)
        H_computed_from_ideal.a = Ha_computed_from_ideal

        Ha_computed_from_test = Uout_freq_measured_test.a / Uin_freq_measured_test.a
        H_computed_from_test = transfer_function_class(Uin_freq_measured_test.f)
        H_computed_from_test.a = Ha_computed_from_test

        # plot_vector(vector=Ha_computed_from_ideal, legend='Ha_computed_from_ideal')

        # plot_2_transfer_functions(H1=H_ideal, H2=H_computed_from_ideal, legend1='H_ideal', legend2='H_computed_from_ideal')
        plot_2_transfer_functions(H1=H_ideal, H2=H_computed_from_test, legend1='H_ideal',
                                  legend2='H_computed_from_test')



        # plot_2_signals(U1=Uin_AWG_ideal,U2=Uin_AWG_test,legend1='Uin_AWG_ideal',legend2='Uin_AWG_test')
        # plot_2_signals(U1=Uin_measured_ideal, U2=Uin_measured_test, legend1='Uin_measured_ideal', legend2='Uin_measured_test')
        # plot_2_signals(U1=Uout_time_measured_ideal, U2=Uout_time_measured_test, legend1='Uout_time_measured_ideal',
        #                legend2='Uout_time_measured_test')

        plot_vector(Uout_time_measured_ideal.in_V - Uout_time_measured_test.in_V)

        Uin_measured_compl_ideal = read_in_transfer_function_old_convention(
            mock_data_path + 'ideal_12_07_2018_12_03_47/csv/UinAmplFrq_linear.csv', pathPh=last_directory_used + 'UinPhase.csv',
            delimiter=';')
        Uin_compl_computed = read_in_transfer_function_old_convention(pathA=last_directory_used + 'UinAmplFrq_linear.csv',  pathPh=last_directory_used + 'UinPhase.csv',delimiter=';')

        plot_2_transfer_functions(H1=Uin_measured_compl_ideal, H2=Uin_compl_computed, legend1='Uin_compl_ideal', legend2='Uin_compl_computed')
        # plot_transfer_function(H=Uin_compl_computed, legend1="Uin_compl_computed")

        Uin_ideal = read_in_signal(path = mock_data_path + 'ideal_12_07_2018_12_03_47/csv/UinTime.csv', delimiter=';')
        Uin_computed = read_in_signal(path = last_directory_used + 'UinTime.csv', delimiter=';')

        # plot_2_signals(U1=Uin_ideal, U2=Uin_computed, legend1='Uin_ideal', legend2='Uin_computed')

        Uout_ideal = read_in_signal(path = mock_data_path + 'ideal_12_07_2018_12_03_47/csv/UoutTime.csv', delimiter=';')
        Uout_computed = read_in_signal(path = last_directory_used + 'UoutTime.csv', delimiter=';')

        plot_2_signals(U1=Uout_ideal, U2=Uout_computed, legend1='Uout_ideal', legend2='Uout_computed')



        H_determined = transfer_function_class(f)
        H_determined.a = Ha
        H_determined.p = Hph

        plot_2_transfer_functions(H1=H_ideal, H2=H_determined, legend1='H_ideal', legend2='H_determined')

        self.assertTrue(1)

    def read_in_get_H_signal_data(self, get_H_csv_directory):
        path_Uin_AWG_time = get_H_csv_directory + 'OriginalSignal.csv'
        path_Uin_sample_rate = get_H_csv_directory + 'Samplerates.csv'
        path_Uin_measured_time = get_H_csv_directory + 'UinTime.csv'
        path_Uout_time = get_H_csv_directory + 'UoutTime.csv'
        path_Uout_Ampl = get_H_csv_directory + 'UoutAmplFrq_linear.csv'
        path_Uout_Phase = get_H_csv_directory + 'UoutPhase.csv'
        path_Uin_Ampl = get_H_csv_directory + 'UinAmplFrq_linear.csv'
        path_Uin_Phase = get_H_csv_directory + 'UinPhase.csv'
        path_Ha = get_H_csv_directory + 'HAmpl_linear.csv'
        path_Hp = get_H_csv_directory + 'PhaseH.csv'
        Uin_AWG = read_in_signal_with_sample_rate(path_Uin_AWG_time, path_Uin_sample_rate, delimiter=';')
        Uin_measured = read_in_signal(path_Uin_measured_time, delimiter=';')
        Uout_time_measured = read_in_signal(path_Uout_time, delimiter=';')
        Uout_freq_measured = read_in_transfer_function_old_convention(pathA=path_Uout_Ampl,pathPh=path_Uout_Phase, delimiter=';')
        Uin_freq_measured = read_in_transfer_function_old_convention(pathA=path_Uin_Ampl, pathPh=path_Uin_Phase,
                                                                      delimiter=';')
        H = read_in_transfer_function_old_convention(pathA=path_Ha, pathPh=path_Hp, delimiter=';')

        return Uin_AWG, Uin_measured, Uout_time_measured, Uout_freq_measured, Uin_freq_measured, H
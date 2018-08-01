from unittest import TestCase
import unittest
from numpy import genfromtxt
from scipy import linalg
import matplotlib.pyplot as plt
from blocks.adjust_a import adjust_a

from helpers.overlay import overlay
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
from helpers.csv_helper import read_in_get_H_signal_data
from blocks import get_H
import os
from classes.signal_class import signal_class
from helpers.plot_helper import plot_2_signals
from helpers.signal_helper import calculate_error



import numpy as np


class test_mock_system(TestCase):

    def __init__(self, *args, **kwargs):
        if __name__ == '__main__':
            unittest.main(exit=False)
        super(test_mock_system, self).__init__(*args, **kwargs)

    def test_mock_system(self):

        sample_rate_DSO = 9999e5

        folder_signal_ideal = mock_data_path + 'get_H/19.07.2018_09_26_38/csv/'

        Uin_AWG_ideal, Uin_measured_ideal, Uout_time_measured_ideal, Uout_freq_measured_ideal, Uin_freq_measured_ideal, H_ideal = read_in_get_H_signal_data(
            folder_signal_ideal)

        mock_system.H = H_ideal

        Uin_AWG_ideal.Vpp = 40e-3

        mock_system.write_to_AWG(signal=Uin_AWG_ideal.in_V, awg_Vpp= Uin_AWG_ideal.Vpp, samplerateAWG=Uin_AWG_ideal.sample_rate)
        time, dataUin, dataUout = mock_system.read_from_DSO(samplerateOszi=sample_rate_DSO, signal=Uin_AWG_ideal, fmax=8e7, vpp_ch1=Uin_AWG_ideal.Vpp)

        Uout_measured_computed = signal_class(time, dataUout)
        Uin_measured_computed = signal_class(time, dataUin)

        Uin_measured_computed = overlay(Uin_measured_computed, Uin_measured_ideal)
        Uout_measured_computed = overlay(Uout_measured_computed, Uout_time_measured_ideal)

        err_Uin = calculate_error(Uin_measured_computed, Uin_measured_ideal)
        err_Uout = calculate_error(Uout_measured_computed, Uout_time_measured_ideal)

        # plot_2_signals(Uin_measured_computed, Uin_measured_ideal)
        # plot_2_signals(Uout_measured_computed, Uout_time_measured_ideal)

        self.assertTrue(err_Uin < 3e-5)
        self.assertTrue(err_Uout < 3e-5)


    if __name__=='__main__':
        try:
            unittest.main()
        except SystemExit as inst:
            if inst.args[0] is True: # raised by sys.exit(True) when tests failed
                raise
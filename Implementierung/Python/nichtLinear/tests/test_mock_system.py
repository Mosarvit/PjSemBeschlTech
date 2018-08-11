import unittest
from unittest import TestCase

from classes.signal_class import signal_class
from helpers.csv_helper import read_in_get_H_signal_data, read_in_signal
from helpers.overlay import overlay
from helpers.tezt_helper import finilize_tezt
from helpers.plot_helper import plot_2_signals
from settings import mock_data_path
from settings import mock_system


class test_mock_system(TestCase):

    def __init__(self, *args, **kwargs):
        if __name__ == '__main__':
            unittest.main(exit=False)
        super(test_mock_system, self).__init__(*args, **kwargs)

    def test_mock_system_Uin(self):

        sample_rate_DSO = 9999e5

        folder_signal_ideal = mock_data_path + 'get_H/19.07.2018_09_26_38/csv/'

        Uin_AWG_ideal, Uin_measured_ideal, Uout_time_measured_ideal, Uout_freq_measured_ideal, Uin_freq_measured_ideal, H_ideal = read_in_get_H_signal_data(
            folder_signal_ideal)

        mock_system.H = H_ideal

        Uin_AWG_ideal.Vpp = 40e-3

        mock_system.write_to_AWG(signal=Uin_AWG_ideal.in_V, awg_Vpp= Uin_AWG_ideal.Vpp, samplerateAWG=Uin_AWG_ideal.sample_rate)
        time, dataUin, dataUout = mock_system.read_from_DSO(samplerateOszi=sample_rate_DSO, signal=Uin_AWG_ideal, fmax=8e7, vpp_ch1=Uin_AWG_ideal.Vpp)

        Uin_measured_computed = signal_class(time, dataUin)
        Uin_measured_computed = overlay(Uin_measured_computed, Uin_measured_ideal)

        test_succeeded = finilize_tezt(values_computed=Uin_measured_computed, set_accepted_values=0, verbosity=0)
        self.assertTrue(test_succeeded)

    def test_mock_system_Uout(self):
        sample_rate_DSO = 9999e5

        folder_signal_ideal = mock_data_path + 'get_H/19.07.2018_09_26_38/csv/'

        Uin_AWG_ideal, Uin_measured_ideal, Uout_time_measured_ideal, Uout_freq_measured_ideal, Uin_freq_measured_ideal, H_ideal = read_in_get_H_signal_data(
            folder_signal_ideal)

        mock_system.H = H_ideal

        Uin_AWG_ideal.Vpp = 40e-3

        mock_system.write_to_AWG(signal=Uin_AWG_ideal.in_V, awg_Vpp=Uin_AWG_ideal.Vpp,
                                 samplerateAWG=Uin_AWG_ideal.sample_rate)
        time, dataUin, dataUout = mock_system.read_from_DSO(samplerateOszi=sample_rate_DSO, signal=Uin_AWG_ideal,
                                                            fmax=8e7, vpp_ch1=Uin_AWG_ideal.Vpp)

        Uout_measured_computed = signal_class(time, dataUin)
        Uout_measured_computed = overlay(Uout_measured_computed, Uout_time_measured_ideal)

        test_succeeded = finilize_tezt(values_computed=Uout_measured_computed, set_accepted_values=0,
                                       verbosity=0)
        self.assertTrue(test_succeeded)



    if __name__=='__main__':
        try:
            unittest.main()
        except SystemExit as inst:
            if inst.args[0] is True: # raised by sys.exit(True) when tests failed
                raise
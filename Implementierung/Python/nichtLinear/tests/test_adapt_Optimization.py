from unittest import TestCase
from helpers.adapt_Optimization import zero_padding
from blocks.generate_BBsignal import generate_BBsignal
import numpy as np
import matplotlib.pyplot as plt
from helpers.FFT import spectrum_from_TimeSignal, spectrum_from_Time_Signal_ZeroPadding
"""
This test-class is to test the functions which offer functionality to manipulate data used in the optimization processes.
"""





class test_adapt_Optimization(TestCase):


    def __init__(self, *args, **kwargs):
        super(test_adapt_Optimization, self).__init__(*args, **kwargs)

    def test_zero_padding_300(self):

        f_rep = 900e3
        f_BB = 5e6
        Vpp = 0.3

        sample_rate_AWG_max = 2e8
        sample_rate_DSO = 9999e5

        Uout_ideal = generate_BBsignal(f_rep=f_rep, f_BB=f_BB, Vpp=Vpp, sample_rate_AWG_max=sample_rate_AWG_max,
                                       verbosity=0)

        U_appended = zero_padding(Uout_ideal, 300)
        delta_t_appended = U_appended.time[-1] / (U_appended.length - 1)
        delta_t_ideal = Uout_ideal.time[-1] / (Uout_ideal.length - 1)
        if delta_t_appended != delta_t_ideal:
            self.assertTrue(False, 'test zero padding: timestep differs between original and paddingd signal')
        last_values = U_appended.in_V[-300: ]
        middle_values = U_appended.in_V[300: -300]
        first_values = U_appended.in_V[0: 300]
        if any(middle_values != Uout_ideal.in_V):
            self.assertTrue(False, 'test zero padding: first values are not equal to initial values')
        if any(last_values != np.zeros(300)) or any(first_values != np.zeros(300)):
            self.assertTrue(False, 'test zero padding: added values are not added with zero')

        test_succeeded = True
        self.assertTrue(test_succeeded)

    def test_zero_padding_with_FFT(self):
        f_rep = 900e3
        f_BB = 5e6
        Vpp = 0.3

        sample_rate_AWG_max = 2e8
        sample_rate_DSO = 9999e5

        Uout_ideal = generate_BBsignal(f_rep=f_rep, f_BB=f_BB, Vpp=Vpp, sample_rate_AWG_max=sample_rate_AWG_max,
                                       verbosity=0)

        U_appended = zero_padding(Uout_ideal, Uout_ideal.length)

        frequencies_orig, spectrum_orig = spectrum_from_TimeSignal(Uout_ideal.time, Uout_ideal.in_V)
        frequencies_appended, spectrum_appended = spectrum_from_TimeSignal(U_appended.time, U_appended.in_V)
        multiplied_spectrum = spectrum_appended * U_appended.length / Uout_ideal.length

        frequencies, spectrum = spectrum_from_Time_Signal_ZeroPadding(time=Uout_ideal.time, values=Uout_ideal.in_V, number=Uout_ideal.length)

        frequencies_new, normalized_spectrum = spectrum_from_Time_Signal_ZeroPadding(Uout_ideal.time, Uout_ideal.in_V, Uout_ideal.length)
        plt.plot(frequencies, np.abs(spectrum), 'r', frequencies_appended, np.abs(multiplied_spectrum), 'b')
        plt.show()
        plt.plot(frequencies_orig, abs(spectrum_orig), 'r', frequencies_appended, abs(spectrum_appended), 'r', frequencies_appended, np.abs(multiplied_spectrum), 'g', frequencies_new, np.abs(normalized_spectrum), 'y')
        plt.show()
        plt.plot(frequencies_orig, np.angle(spectrum_orig, deg=True), 'r', frequencies_appended, np.angle(spectrum_appended, deg=True), 'b')
        plt.show()

        test_succeeded = True
        self.assertTrue(test_succeeded)




from classes.transfer_function_class import transfer_function_class
from classes.signal_class import signal_class
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import time
import copy

from helpers.FFT import spectrum_from_TimeSignal


def adjust_H(Halt, Uout_ideal, Uout_measured, sigma_H, verbosity=False, savePLOT=False):
    """
    adjust_H adopts transfer function H by comparing desired and received Output (Gain) Voltage.
    This implementation uses a simple first approach in adjusting abs(H).
    It offers two ideas to reduce problems caused by noise, discretization and interpolation.
    See report for information.

    INPUT:

        Halt - Instance of transfer_funtion:
            Halt.f - frequencies f
            Halt.a - amplifying factors a
            Halt.p - phase shifts p
            Halt.c - Complex Value c = a*exp(jp)

        U_ideal.csv.csv.csv.csv - the desired output Voltage (BB-Signal, normally single-sine), Instance of signal_class

            Instance of signal_class:
            U.time          - get time vector
            U.in_V          - get signal vector in V
            U.in_mV         - get signal vector in mV
            U.sample_rate   - get sample rate
            U.Vpp           - get Vpp
            U.length        - get length of the signal

        Uout_measured - the measured output Voltage to be compared with U_ideal.csv.csv.csv.csv, instance of signal_class

        sigma_H - scalar; step to iterate (positive)

        verbosity - if True, plots are shown (slows down program, enabling debugging and results on the road)

    OUTPUT:

        Heu - Instance of transfer_funtion:
            Hneu.f - frequencies f
            Hneu.a - amplifying factors a
            Hneu.p - phase shifts p
            Hneu.c - Complex Value c = a*exp(jp)

    """

    type_check_adjust_H(Halt, Uout_ideal, Uout_measured, sigma_H)

    if verbosity:
        delta_t_meas = Uout_measured.time[1] - Uout_measured.time[0]
        delta_t_id = Uout_ideal.time[1] - Uout_ideal.time[0]
        # Plot voltages
        plt.scatter(Uout_ideal.time, Uout_ideal.in_V, c='r', marker=".")
        plt.scatter(Uout_measured.time, Uout_measured.in_V, c='b', marker=".")
        plt.title('U_ideal.csv.csv.csv.csv - red, Uout_meas - blue')
        plt.xlabel('t')
        plt.ylabel('U')
        plt.suptitle('Number of points: ' + str(len(Uout_ideal.time)) + ' ideal, ' + str(len(Uout_measured.time)) + ' meas')
        plt.suptitle('Timestep Meas: ' + str(delta_t_meas) +  ' Timestep Ideal: ' + str(delta_t_id) )
        plt.xlim((Uout_ideal.time[0], Uout_ideal.time[-1]))
        plt.show()
     

    # calculate Spectrum:
    frequencies_Id, spectrum_Id = spectrum_from_TimeSignal(Uout_ideal.time, Uout_ideal.in_V)
    frequencies_Meas, spectrum_Meas = spectrum_from_TimeSignal(Uout_measured.time, Uout_measured.in_V)

    # reduce to lower describable frequency:
    fmax_to_use = np.minimum(frequencies_Meas[-1], frequencies_Id[-1])
    idx_max_Id = np.where(frequencies_Id <= fmax_to_use)[0][-1]  # where returns tuple
    idx_max_Meas = np.where(frequencies_Meas <= fmax_to_use)[0][-1]
    frequencies_Id = frequencies_Id[0:idx_max_Id]
    frequencies_Meas = frequencies_Meas[0:idx_max_Meas]
    spectrum_Id = spectrum_Id[0:idx_max_Id]
    spectrum_Meas = spectrum_Meas[0:idx_max_Meas]

    # check frequency range of signal. If less frequencies than in H,
    # add frequency in signal with amplitude 1 s.t. signal has frequencies >= H
    # (default_value is just what you like to have as default value, calculated to enable Plots showing senseful scale)
    default_value = np.minimum(np.min(abs(spectrum_Id)), np.min(abs(spectrum_Meas)))
    if default_value == 0:
        default_value = 1e-4 # avoids problems by dividing through 0
    delta_f_Id = frequencies_Id[1] - frequencies_Id[0]
    delta_f_Meas = frequencies_Meas[1] - frequencies_Meas[0]
    if np.amax(Halt.f) > frequencies_Meas[-1]:
        numberOfNewPoints = np.int(np.ceil((np.max(Halt.f) - frequencies_Meas[-1]) / delta_f_Meas))
        newFrequencies = np.linspace(frequencies_Meas[-1] + delta_f_Meas,
                                     frequencies_Meas[-1] + numberOfNewPoints * delta_f_Meas, numberOfNewPoints)
        frequencies_Meas = np.append(frequencies_Meas, newFrequencies)
        spectrum_Meas = np.append(spectrum_Meas, np.ones(numberOfNewPoints) * default_value)

    if (np.amax(Halt.f) > frequencies_Id[-1]):
        numberOfNewPoints = np.int(np.ceil((np.max(Halt.f) - frequencies_Id[-1]) / delta_f_Id))
        newFrequencies = np.linspace(frequencies_Id[-1] + delta_f_Id,
                                     frequencies_Id[-1] + numberOfNewPoints * delta_f_Id, numberOfNewPoints)
        frequencies_Id = np.append(frequencies_Id, newFrequencies)
        spectrum_Id = np.append(spectrum_Id, np.ones(numberOfNewPoints) * default_value)


    #####
    Id_spectrum = signal_class(frequencies_Id, spectrum_Id)
    Meas_spectrum = signal_class(frequencies_Meas, spectrum_Meas)
    # just to enable return for report 2018!
    ##### end

    # to reduce WHITE NOISE: clear lowest percentage of signal amplitudes
    # set ratio (percentage) to any desired value
    # TODO: add input parameter with ratio to not define it here
    ratio_ideal = 10e-3
    ratio_meas = 10e-3
    # find indices to set to default:
    idx_clear_Id = np.where(abs(spectrum_Id) <= ratio_ideal * np.max(abs(spectrum_Id)))[0]
    idx_clear_Meas = np.where(abs(spectrum_Meas) <= ratio_meas * np.max(abs(spectrum_Meas)))[0]
    # cross-referencing frequencies s.t. default values are at same frequencies
    idx_clear_crossref_Id = np.around(frequencies_Meas[idx_clear_Meas] / delta_f_Id).astype(int)
    idx_clear_crossref_Meas = np.round(frequencies_Id[idx_clear_Id] / delta_f_Meas).astype(int)
    # check for length of idx in cross-referencing
    if idx_clear_crossref_Id.size:
        if np.max(idx_clear_crossref_Id) > len(spectrum_Id) - 1:
            idx_clear_crossref_Id = idx_clear_crossref_Id[0: len(spectrum_Id) - 1]
    if idx_clear_crossref_Meas.size:
        if np.max(idx_clear_crossref_Meas) > len(spectrum_Meas) - 1:
            idx_clear_crossref_Meas = idx_clear_crossref_Meas[np.where(idx_clear_crossref_Meas < len(spectrum_Meas))]

    # set values to default
    spectrum_Id[idx_clear_Id] = default_value * np.ones(len(idx_clear_Id))
    spectrum_Meas[idx_clear_Meas] = default_value * np.ones(len(idx_clear_Meas))
    spectrum_Id[idx_clear_crossref_Id] = default_value * np.ones(len(idx_clear_crossref_Id))
    spectrum_Meas[idx_clear_crossref_Meas] = default_value * np.ones(len(idx_clear_crossref_Meas))

    # interpolate magnitude and phase seperately
    magnitude_Ideal = interp1d(frequencies_Id, np.abs(spectrum_Id), kind='linear')
    angle_ideal = interp1d(frequencies_Id, np.angle(spectrum_Id), kind='linear')
    magnitude_Meas = interp1d(frequencies_Meas, np.abs(spectrum_Meas), kind='linear')
    angle_meas = interp1d(frequencies_Meas, np.angle(spectrum_Meas), kind='linear')

    # calculate separately for amplitude and angle
    ratio_abs = magnitude_Meas(Halt.f) / magnitude_Ideal(Halt.f) - 1
    diff_angle = angle_meas(Halt.f) - angle_ideal(Halt.f)

    ###
    # just to enable return for report 2018!
    fabs_orig = copy.copy(ratio_abs)
    ###

    # to reduce WHITE NOISE attempt 2:
    # cut high amplifying ratios (over RMS)
    # TODO: add input parameter use_rms to not define it here
    # use just non-zero values in ratio_abs to calculate rms because of above used setter to reduce white noise
    # setting white-noise values to cause zeros in ratio_abs but just to enable changes in Hneu.a
    use_rms = True
    rms = np.sqrt(np.mean(np.square(ratio_abs)))
    ###
    # just to enable return for report 2018!
    rms_orig = copy.copy(rms)
    ###
    values = ratio_abs[np.where(abs(ratio_abs) >= 0.02 * rms)[
        0]]  # just guessing: 2 % of original rms as interpolated results of white-noise adopted values in signals
    rms = np.sqrt(np.mean(np.square(values)))
    if use_rms:
        # find indices to set to 1:
        idx_clear = np.where(abs(ratio_abs) > rms)[0]
        if not (len(idx_clear) == len(ratio_abs)):  # check for simple signals with Uout_Id = multiple Uout_Meas
            ratio_abs[idx_clear] = np.zeros(len(idx_clear))
            diff_angle[idx_clear] = np.zeros(len(idx_clear))


    # now using new convention with classes transfer_function for frequency and complex-values connecting variables
    ### just using convention here!
    complex_ratio = transfer_function_class(Halt.f)
    complex_ratio.a = ratio_abs
    complex_ratio.p = diff_angle
    complex_spectrum_Id = transfer_function_class(frequencies_Id) # complex spectrum
    complex_spectrum_Id.c = spectrum_Id
    complex_spectrum_Meas = transfer_function_class(frequencies_Meas)
    complex_spectrum_Meas.c = spectrum_Meas

    # initialize Hneu
    Hneu = transfer_function_class(Halt.f)
    Hneu.a = Halt.a * (1 + sigma_H * complex_ratio.a)
    Hneu.p = Halt.p + sigma_H * complex_ratio.p
  

    if verbosity:

        # Plot Magnitudes:
            
            #plot gsi
        #plt.subplot(2, 3, 1)
        plt.plot(frequencies_Id, abs(spectrum_Id), 'r', frequencies_Meas, abs(spectrum_Meas), 'b')
        plt.title('ABS(FFT): Ideal rot, Meas blau')
        plt.xlabel('f')
        plt.ylabel('Ampl')
        plt.xlim((0, np.max(Halt.f)))
        plt.ylim((0, 1e-3))
        plt.show()
    #
#       # plt.subplot(2, 3, 4)
        plt.plot(Halt.f, rms * np.ones(len(Halt.f)), 'r', Halt.f, -rms * np.ones(len(Halt.f)), 'r')
       #plt.xlim((0, np.max(Halt.f)))
       #plt.ylim((-rms * 3, 3 * rms))

       #plt.subplot(2, 3, 4)
        plt.plot(Halt.f, ratio_abs, 'b')
        plt.xlim((0, np.max(Halt.f)))
        plt.ylim((-rms * 3, 3 * rms))
        plt.title('Absratio Umeas / Uideal -1')
        plt.xlabel('f')
        plt.ylabel('ratio')

        if use_rms:
            plt.plot(Halt.f, rms * np.ones(len(Halt.f)), 'r', Halt.f, -rms*np.ones(len(Halt.f)), 'r')
            plt.xlim((0, np.max(Halt.f)))

        plt.show()

        #plt.subplot(2, 3, 2)
        plt.plot(Halt.f, Halt.a, 'r', Hneu.f, Hneu.a, 'b')
        plt.title('Abs(H): alt rot - neu blau')
        plt.xlabel('f')
        plt.ylabel('Magnitude')
        plt.xlim((0, np.max(Halt.f)))
        plt.show()

# #        plt.subplot(2, 3, 3)
        plt.plot(frequencies_Id, complex_spectrum_Id.p, 'r', frequencies_Meas, complex_spectrum_Meas.p, 'b')
        plt.title('ANGLE(FFT): Ideal rot - Meas blau')
        plt.xlabel('f')
        plt.ylabel('Angle')
        plt.xlim((0, np.max(Halt.f)))
        plt.ylim((-50, 50))
        plt.show()
#
# #        plt.subplot(2, 3, 6)
        plt.plot(Halt.f, complex_ratio.p)
        plt.title('Anglediff Umeas/Uideal')
        plt.xlabel('f')
        plt.ylabel('ratio')
        plt.xlim((0, np.max(Halt.f)))
        plt.show()

#         # Plot H
# #        plt.subplot(2, 3, 5)
#         plt.plot(Halt.f, Halt.p, 'r', Hneu.f, Hneu.p, 'b')
#         plt.title('Angle(H): alt rot - neu blau')
#         plt.xlabel('f')
#         plt.ylabel('angle')
#         plt.xlim((0, np.max(Halt.f)))
#         plt.show()
#         if savePLOT:
#             fig.savefig('../data/adjustH/plots/routine' + str(time.strftime("%d%m_%H%M")) + '.pdf')
#         # fig.savefig('../../data/adjustH/plots/adjust_Plots' + time.strftime("%H%M_%d%m")+ '.pdf')

    return (Hneu) #, ratio_abs, Id_spectrum, Meas_spectrum, rms, rms_orig)



def type_check_adjust_H(Halt, Uout_ideal, Uout_measured, sigma_H):

    """
    does the type-checking of input values in adjust_H.
    :param Halt: instance of transfer_cuntion
    :param Uout_ideal: instance of signal
    :param Uout_measured: instance of signal
    :param sigma_H: scalar vector - no type-check by now
    :return: no output
    """
    if not isinstance(Halt, transfer_function_class):
        raise ValueError('old transfer-function has to be instance of class transfer_function_class.'
                         'See documentation of class for information about creating an instance.')
    if not isinstance(Uout_measured, signal_class):
        raise ValueError('measured signal has to be instance of class signal_class.'
                         'See documentaion of class for information about creating an instance.')
    if not isinstance(Uout_ideal, signal_class):
        raise ValueError('ideal signal has to be instance of class signal_class.'
                         'See documentaion of class for information about creating an instance.')

    return
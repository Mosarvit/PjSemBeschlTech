from classes.transfer_function_class import transfer_function_class
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import time
import copy


def adjust_H(Halt, Uout_ideal, Uout_measured, sigma_H, verbosity=False, savePLOT=False):
    """
    adjust_H adopts transfer function H by comparing desired and received Output (Gain) Voltage

    INPUT:

        Halt - nx3 array; old transferfuntion (n - number of frequencies)
            Halt[:,0] - frequencies f
            Halt[:,1] - amplifying factors
            Halt[:,2] - phase shifts

            Instance of transfer_funtion:
            Halt.f - frequencies f
            Halt.a - amplifying factors a
            Halt.p - phase shifts p
            Halt.c - Complex Value c = a*exp(jp)

        Uout_ideal - nx2 array; U_? (n - length of signal)
            Uout_ideal[:,0] - time-axis
            Uout_ideal[:,1] - voltage

        Uout_measured - nx2 array; (n - length of signal)
            Uout_measured[:,0] - time-axis
            Uout_measured[:,1] - voltage

        sigma_H - scalar; step to iterate

        verbosity - if True, plots are shown (slows down program,  enabling debugging and results on the road)

    OUTPUT:

        Heu - nx3 array; new transferfuntion (n - number of frequencies)
            Hneu[:,0] - frequencies f
            Hneu[:,1] - amplifying factors
            Hneu[:,2] - phase shifts

            Instance of transfer_funtion:
            Hneu.f - frequencies f
            Hneu.a - amplifying factors a
            Hneu.p - phase shifts p
            Hneu.c - Complex Value c = a*exp(jp)

    """

    # validate Halt as instance of transfer_function
    if not isinstance(Halt, transfer_function_class):
        raise TypeError('Uncorrect function call of adjust_H with Halt no instance of class transfer_funtion')

    if verbosity:
        delta_t_meas = Uout_measured.time[1] - Uout_measured.time[0]
        delta_t_id = Uout_ideal.time[1] - Uout_ideal.time[0]
        #print('Zeitstep Meas: ' + str(delta_t_meas) +  ' Zeitstep Ideal: ' + str(delta_t_id) )
        fig = plt.figure()
        # Plot Spannungen
        plt.scatter(Uout_ideal.time, Uout_ideal.in_V, c='r', marker=".")
        plt.scatter(Uout_measured.time, Uout_measured.in_V, c='b', marker=".")
        plt.title('Uout_ideal - rot, Uout_meas - blau')
        plt.xlabel('t')
        plt.ylabel('U')
        plt.suptitle('Number of points: ' + str(len(Uout_ideal.time)) + ' ideal, ' + str(len(Uout_measured.time)) + ' meas')
        plt.suptitle('Zeitstep Meas: ' + str(delta_t_meas) +  ' Zeitstep Ideal: ' + str(delta_t_id) )
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
        default_value = 1e-4
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

    # to reduce WHITE NOISE: clear lowest percentage of signal amplitudes
    # set ratio (percentage) to any desired value
    ratio_ideal = 0#5e-3
    ratio_meas = 0#5e-3
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

    # initialize Hneu
    Hneu = transfer_function_class(Halt.f)

    # old - malfunctioning:
    # calculate Hneu in complex representation
    #    Umeas_div_Uid = magnitude_Meas(Halt.f) / magnitude_Ideal(Halt.f) * np.exp( 1j * (angle_meas(Halt.f) - angle_ideal(Halt.f) ) )
    # Hneu.c = Halt.c * (1 + sigma_H * (Umeas_div_Uid - 1))

    # better Attempt: calculate separately for amplitude and angle
    ratio_abs = magnitude_Meas(Halt.f) / magnitude_Ideal(Halt.f) - 1
    diff_angle = angle_meas(Halt.f) - angle_ideal(Halt.f)
    
    

    # to reduce WHITE NOISE attempt 2:
    # cut high amplifying ratios (over RMS)
    use_rms = True
    # use just non-zero values in ratio_abs to calculate rms because of above used setter to reduce white noise
    # setting white-noise values to cause zeros in ratio_abs but just to enable changes in Hneu.a
    rms = np.sqrt(np.mean(np.square(ratio_abs)))
    values = ratio_abs[np.where(abs(ratio_abs) >= 0.02 * rms)[
        0]]  # just guessing: 2 % of original rms as interpolated results of white-noise adopted values in signals
    rms = np.sqrt(np.mean(np.square(values)))
    if use_rms:
        # find indices to set to 1:
        idx_clear = np.where(abs(ratio_abs) > rms)[0]
        if not (len(idx_clear) == len(ratio_abs)):  # check for simple signals with Uout_Id = multiple Uout_Meas
            ratio_abs[idx_clear] = np.zeros(len(idx_clear))
            diff_angle[idx_clear] = np.zeros(len(idx_clear))
            
    H = transfer_function_class(Halt.f)
    H.a = ratio_abs
    H.p = diff_angle
    H_id = transfer_function_class(frequencies_Id)
    H_id.c = spectrum_Id
    H_Meas = transfer_function_class(frequencies_Meas)
    H_Meas.c = spectrum_Meas

    Hneu.a = Halt.a * (1 - sigma_H * H.a)
    Hneu.p = Halt.p #- sigma_H * H.p
  

    if verbosity:
        fig = plt.figure(1)
        # Plot Magnitudes:
            
            #plot gsi
        #plt.subplot(2, 3, 1)
#        plt.plot(frequencies_Id, abs(spectrum_Id), 'r', frequencies_Meas, abs(spectrum_Meas), 'b')
#        plt.title('ABS(FFT): Ideal rot, Meas blau')
#        plt.xlabel('f')
#        plt.ylabel('Ampl')
#        plt.xlim((0, np.max(Halt.f)))
#        plt.ylim((0, 1e-3))
#        plt.show()
#
#       # plt.subplot(2, 3, 4)
#        plt.plot(Halt.f, rms * np.ones(len(Halt.f)), 'r', Halt.f, -rms * np.ones(len(Halt.f)), 'r')
#        #plt.xlim((0, np.max(Halt.f)))
#        #plt.ylim((-rms * 3, 3 * rms))
#        
#        #plt.subplot(2, 3, 4)
#        plt.plot(Halt.f, ratio_abs, 'b')
#        plt.xlim((0, np.max(Halt.f)))
#        plt.ylim((-rms * 3, 3 * rms))
#        plt.title('Absratio Umeas / Uideal -1')
#        plt.xlabel('f')
#        plt.ylabel('ratio')
#        plt.show()

        # if use_rms:
        #     plt.subplot(2, 3, 4)
        #     plt.plot(Halt.f, rms * np.ones(len(Halt.f)), 'r', Halt.f, -rms*np.ones(len(Halt.f)), 'r')
        #     plt.xlim((0, np.max(Halt.f)))

        #plt.subplot(2, 3, 2)
        plt.plot(Halt.f, Halt.a, 'r', Hneu.f, Hneu.a, 'b')
        plt.title('Abs(H): alt rot - neu blau')
        plt.xlabel('f')
        plt.ylabel('Magnitude')
        plt.xlim((0, np.max(Halt.f)))
        plt.show()

#        plt.subplot(2, 3, 3)
        plt.plot(frequencies_Id, H_id.p, 'r', frequencies_Meas, H_Meas.p, 'b')
        plt.title('ANGLE(FFT): Ideal rot - Meas blau')
        plt.xlabel('f')
        plt.ylabel('Angle')
        plt.xlim((0, np.max(Halt.f)))
        plt.ylim((-50, 50))
        plt.show()

#        plt.subplot(2, 3, 6)
        plt.plot(Halt.f, H.p)
        plt.title('Anglediff Umeas/Uideal')
        plt.xlabel('f')
        plt.ylabel('ratio')
        plt.xlim((0, np.max(Halt.f)))
        plt.show()

        # Plot H
#        plt.subplot(2, 3, 5)
        plt.plot(Halt.f, Halt.p, 'r', Hneu.f, Hneu.p, 'b')
        plt.title('Angle(H): alt rot - neu blau')
        plt.xlabel('f')
        plt.ylabel('angle')
        plt.xlim((0, np.max(Halt.f)))
        plt.show()
        if savePLOT:
            fig.savefig('../data/adjustH/plots/routine' + str(time.strftime("%d%m_%H%M")) + '.pdf')
        # fig.savefig('../../data/adjustH/plots/adjust_Plots' + time.strftime("%H%M_%d%m")+ '.pdf')

    return (Hneu)


def spectrum_From_FFT(frequencies, fft_norm):
    """
    calculates the frequency axis and the spectrum usable for a real signal by applying Nyquists Theorem
    :param frequencies: the frequency axis, evenly spaced, increasing orderd
    :param fft_norm: the fft of a time signal generated by numpy.fft(...)
    :return: the spectrum and frequencies reduced to the describable frequency-range (Nyquist)
    """

    # check length
    if len(frequencies) != len(fft_norm):
        raise TypeError('Frequency and FFT have to contain same number of values')

    # find max Frequencies (Nyquists theorem):
    idx_half = int(np.floor(len(fft_norm) / 2))
    # cut frequencies and FFTs to new Range -> only relevant frequencies ocurring
    frequencies = frequencies[0:idx_half]
    spectrum = fft_norm[0:idx_half] / len(fft_norm)

    return (frequencies, spectrum)


def spectrum_from_TimeSignal(time, values):
    """

    :param time: evenly spaced time array
    :param values: real values raised at points in time
    :return: frequency axis, complex spectrum of phaseshift and amplifier(c = abs(c) * exp(1j * np.angle(c)) )
    """
    # check length
    if len(time) != len(values):
        raise TypeError('Time-Array and Values have to contain same number of values')

    # check if values not complex
    # check if time evenly spaced

    delta_f = 1 / (time[-1] - time[0])
    N = len(time)
    frequencies = np.linspace(0, N * delta_f, N)
    frequencies, spectrum = spectrum_From_FFT(frequencies, np.fft.fft(values))

    return (frequencies, spectrum)
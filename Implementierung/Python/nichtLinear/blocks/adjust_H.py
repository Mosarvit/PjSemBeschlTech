from adts.transfer_function import transfer_function
import numpy as np
from scipy.interpolate import interp1d
import matplotlib.pyplot as plt
import time

def adjust_H(Halt, Uout_ideal, Uout_measured, sigma_H, verbosity=False):
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

    #validate Halt as instance of transfer_function
    if not isinstance(Halt, transfer_function):
        raise TypeError('Uncorrect function call of adjust_H with Halt no instance of class transfer_funtion')


    if verbosity:
        delta_t_meas = (Uout_measured[1,0] - Uout_measured[0,0])
        delta_t_id = (Uout_ideal[1,0] - Uout_ideal[0,0])
        print('Zeitstep Meas: ' + str(delta_t_meas) +  ' Zeitstep Ideal: ' + str(delta_t_id) )
        fig = plt.figure()
        # Plot Spannungen
        plt.plot(Uout_ideal[:, 0], Uout_ideal[:, 1], 'r', Uout_measured[:, 0], Uout_measured[:, 1], 'b')
        plt.title('Uout_ideal - rot, Uout_meas - blau')
        plt.xlabel('t')
        plt.ylabel('U')
        plt.show()

    # FFT (normalized) -> complex values divided by Number of Values
    frequencies_Id, Ideal_fft = spectrum_from_TimeSignal(Uout_ideal[:, 0], Uout_ideal[:, 1])
    frequencies_Meas, Meas_fft = spectrum_from_TimeSignal(Uout_measured[:, 0], Uout_measured[:, 1])

    # reduce to lower describable frequency:
    fmax_to_use = np.minimum(frequencies_Meas[-1], frequencies_Id[-1])
    idx_max_Id = np.array(np.where(frequencies_Id <= fmax_to_use))[0, -1]
    idx_max_Meas = np.array(np.where(frequencies_Meas <= fmax_to_use))[0, -1]
    frequencies_Id = frequencies_Id[0:idx_max_Id]
    frequencies_Meas = frequencies_Meas[0:idx_max_Meas]
    Ideal_fft = Ideal_fft[0:idx_max_Id]
    Meas_fft = Meas_fft[0:idx_max_Meas]
    
    # check frequency range of signal. If less frequencies than in H,
    # add frequency in signal with amplitude 1 s.t. signal has frequencies >= H
    # (factor is just what you like to have as default value, calculated to enable Plots showing senseful scale)
    factor = np.minimum(np.min(abs(Ideal_fft)), np.min(abs(Meas_fft)))
    #factor = 1e-4
    delta_f_Id = frequencies_Id[1] - frequencies_Id[0]
    delta_f_Meas = frequencies_Meas[1] - frequencies_Meas[0]
    if np.amax(Halt.f) > frequencies_Meas[-1]:
        numberOfNewPoints = np.int(np.ceil((np.max(Halt.f) - frequencies_Meas[-1]) / delta_f_Meas ))
        newFrequencies = np.linspace(frequencies_Meas[-1]+delta_f_Meas,
                                     frequencies_Meas[-1] + numberOfNewPoints*delta_f_Meas, numberOfNewPoints)
        frequencies_Meas = np.append(frequencies_Meas, newFrequencies)
        Meas_fft = np.append(Meas_fft, np.ones(numberOfNewPoints)*factor)

    if (np.amax(Halt.f) > frequencies_Id[-1]):
        numberOfNewPoints = np.int(np.ceil((np.max(Halt.f) - frequencies_Id[-1]) / delta_f_Id))
        newFrequencies = np.linspace(frequencies_Id[-1] + delta_f_Id,
                                           frequencies_Id[-1] + numberOfNewPoints * delta_f_Id, numberOfNewPoints)
        frequencies_Id = np.append(frequencies_Id, newFrequencies)
        Ideal_fft = np.append(Ideal_fft, np.ones(numberOfNewPoints)*factor)

    # to reduce white noise: clear lowest percentage of signal amplitudes
    # set ratio to any desired value
    ratio_ideal = 0 #3e-3
    ratio_meas = 0 #3e-3
    # find indices to set to default:
    idx_clear_Id = np.array(np.where(abs(Ideal_fft) <= ratio_ideal * np.max(abs(Ideal_fft))))
    idx_clear_Meas = np.array(np.where(abs(Meas_fft) <= ratio_meas * np.max(abs(Meas_fft))))
    # cross-referencing frequencies s.t. default values are at same frequencies
    clearFreq_crossref_Id = np.array(np.round(frequencies_Meas[idx_clear_Meas]/delta_f_Id)).astype(int)
    clearFreq_crossref_Meas = np.array(np.round(frequencies_Id[idx_clear_Id] / delta_f_Meas)).astype(int)
    # set values to default
    Ideal_fft[idx_clear_Id] = factor * np.ones(len(idx_clear_Id))
    Meas_fft[idx_clear_Meas] = factor * np.ones(len(idx_clear_Meas))
    Ideal_fft[clearFreq_crossref_Id] = factor * np.ones(len(clearFreq_crossref_Id))
    Meas_fft[clearFreq_crossref_Meas] = factor * np.ones(len(clearFreq_crossref_Meas))

    # interpolate magnitude and phase seperately
    magnitude_Ideal = interp1d(frequencies_Id, np.abs(Ideal_fft), kind = 'linear' )
    angle_Ideal = interp1d(frequencies_Id, np.angle(Ideal_fft), kind = 'linear' )
    magnitude_Meas = interp1d(frequencies_Meas, np.abs(Meas_fft), kind = 'linear')
    angle_Meas = interp1d(frequencies_Meas, np.angle(Meas_fft), kind = 'linear')

    # initialize Hneu
    Hneu = transfer_function(Halt.f)

    # old - malfunctioning:
    # calculate Hneu in complex representation
#    Umeas_div_Uid = magnitude_Meas(Halt.f) / magnitude_Ideal(Halt.f) * np.exp( 1j * (angle_Meas(Halt.f) - angle_Ideal(Halt.f) ) )
    #Hneu.c = Halt.c * (1 + sigma_H * (Umeas_div_Uid - 1))

    # better Attempt: calculate separately for amplitude and angle
    Ratio_ABS = magnitude_Meas(Halt.f) / magnitude_Ideal(Halt.f) - 1
    Diff_angle = angle_Meas(Halt.f) - angle_Ideal(Halt.f)
    Hneu.a = Halt.a * (1 + sigma_H * Ratio_ABS)
    Hneu.p = Halt.p + sigma_H * Diff_angle

    if verbosity:
        fig = plt.figure(1)
        # Plot Magnitudes:
        plt.subplot(2, 3, 1)
        plt.plot(frequencies_Id, abs(Ideal_fft),'r', frequencies_Meas, abs(Meas_fft), 'b')
        plt.title('ABS(FFT): Ideal rot, Meas blau')
        plt.xlabel('f')
        plt.ylabel('Ampl')
        plt.xlim((0, np.max(Halt.f)))
        plt.ylim((0, 1e-3))

        plt.subplot(2, 3, 4)
        plt.plot(Halt.f, abs(Ratio_ABS))
        plt.title('Absratio Umeas / Uideal -1')
        plt.xlabel('f')
        plt.ylabel('ratio')
        plt.xlim((0, np.max(Halt.f)))

        plt.subplot(2, 3, 2)
        plt.plot(Halt.f, Halt.a, 'r', Hneu.f, Hneu.a, 'b')
        plt.title('Abs(H): alt rot - neu blau')
        plt.xlabel('f')
        plt.ylabel('Magnitude')
        plt.xlim((0, np.max(Halt.f)))

        plt.subplot(2, 3, 3)
        plt.plot(frequencies_Id, np.angle(Ideal_fft), 'r', frequencies_Meas, np.angle(Meas_fft), 'b')
        plt.title('ANGLE(FFT): Ideal rot - Meas blau')
        plt.xlabel('f')
        plt.ylabel('Angle')
        plt.xlim((0, np.max(Halt.f)))

        plt.subplot(2, 3, 6)
        plt.plot(Halt.f, Diff_angle)
        plt.title('Anglediff Umeas/Uideal')
        plt.xlabel('f')
        plt.ylabel('ratio')
        plt.xlim((0, np.max(Halt.f)))

        # Plot H
        plt.subplot(2, 3, 5)
        plt.plot(Halt.f, np.angle(np.exp(1j*Halt.p)), 'r', Hneu.f, np.angle(np.exp(1j*Hneu.p)), 'b')
        plt.title('Angle(H): alt rot - neu blau')
        plt.xlabel('f')
        plt.ylabel('angle')
        plt.xlim((0, np.max(Halt.f)))
        plt.show()
        fig.savefig('../data/adjustH/plots/routine'+str(time.strftime("%d%m_%H%M"))+'.pdf')
        #fig.savefig('../../data/adjustH/plots/adjust_Plots' + time.strftime("%H%M_%d%m")+ '.pdf')

    return(Hneu)


def spectrum_From_FFT(frequencies, fft_norm):
    """
    calculates the frequency axis and the spectrum usable for a real signal by applying Nyquists Theorem
    :param frequencies: the frequency axis
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
    :return: real
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
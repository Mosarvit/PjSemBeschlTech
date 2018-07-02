from adts.transfer_function import transfer_function
import numpy as np
from scipy.interpolate import interp1d

def adjust_H(Halt, Uout_ideal, Uout_measured, sigma_H):
    """
    adjust_H optimiert die Übertragungsfunktion H

    INPUT:

        Halt - nx3 array; die alte Übertragungsfunktion (n - Anzahl der Frequenzen)
            Halt[:,0] - Frequenz f
            Halt[:,1] - Amplitudenverstärkung
            Halt[:,2] - Phasenverschiebung

            Instance of transfer_funtion:
            Halt.f - Frequences f
            Halt.a - Amplitude a
            Halt.p - Phaseshift p
            Halt.c - Complex Value c = a*exp(jp)

        Uout_ideal - nx2 array; U_? (n - Länge des Signals)
            Uout_ideal[:,0] - Zeitvektor
            Uout_ideal[:,1] - Signalvektor

        Uout_measured - nx2 array; (n - Länge des Signals)
            Uout_measured[:,0] - Zeitvektor
            Uout_measured[:,1] - Signalvektor

        sigma_H - skalar; die Schrittweite

    OUTPUT:

        Heu - nx3 array; Übertragungsfunktion (n - Anzahl der Frequenzen)
            Heu[:,0] - Frequenz f
            Heu[:,1] - Amplitudenverstärkung
            Heu[:,2] - Phasenverschiebung

            Instance of transfer_funtion:
            Hneu.f - Frequences f
            Hneu.a - Amplitude a
            Hneu.p - Phaseshift p
            Hneu.c - Complex Value c = a*exp(jp)

    """

    #validate Halt as instance of transfer_function
    if not isinstance(Halt, transfer_function):
        raise TypeError('Uncorrect function call of adjust_H with Halt no instance of class transfer_funtion')

    # create functions of amplitude and phaseshift as interpolations of voltage signals fft
    # frequency distance as inverse time signal length, number of data points, evenly spaced frequency vector as axis of the fft
    delta_f_Meas = 1 / (Uout_measured[-1, 0] - Uout_measured[0, 0])
    N_Meas = len(Uout_measured[:, 0])
    frequencies_Meas = np.linspace(0, N_Meas*delta_f_Meas, N_Meas)
    delta_f_Id = 1 /(Uout_ideal[-1, 0] - Uout_ideal[0, 0])
    N_Id = len(Uout_ideal[:, 0])
    frequencies_Id = np.linspace(0, N_Id*delta_f_Id, N_Id)

    # FFT (normalized) -> complex values divided by Number of Values
    Ideal_fft = np.fft.fft( Uout_ideal[:,1] ) / N_Id
    Meas_fft = np.fft.fft( Uout_measured[:, 1]) / N_Meas

    # check frequency range of signal. If less frequencies than in H, add frequency in signal with amplitude 1 s.t. signal has frequencies >= H
    if np.amax(Halt.f) > frequencies_Meas[-1]:
        numberOfNewPoints = np.int(np.ceil((np.max(Halt.f) - frequencies_Meas[-1]) / delta_f_Meas ))
        newFrequencies = np.linspace(frequencies_Meas[-1]+delta_f_Meas,
                                     frequencies_Meas[-1] + numberOfNewPoints*delta_f_Meas, numberOfNewPoints)
        frequencies_Meas = np.append(frequencies_Meas, newFrequencies)
        Meas_fft = np.append(Meas_fft, np.ones(numberOfNewPoints))

    if (np.amax(Halt.f) > frequencies_Id[-1]):
        numberOfNewPoints = np.int(np.ceil((np.max(Halt.f) - frequencies_Id[-1]) / delta_f_Id))
        newFrequencies = np.linspace(frequencies_Id[-1] + delta_f_Id,
                                           frequencies_Id[-1] + numberOfNewPoints * delta_f_Id, numberOfNewPoints)
        frequencies_Id = np.append(frequencies_Id, newFrequencies)
        Ideal_fft = np.append(Ideal_fft, np.ones(numberOfNewPoints))

    # interpolate magnitude and phase seperately
    magnitude_Ideal = interp1d(frequencies_Id, np.abs(Ideal_fft) )
    angle_Ideal = interp1d(frequencies_Id, np.angle(Ideal_fft) )
    magnitude_Meas = interp1d(frequencies_Meas, np.abs(Meas_fft))
    angle_Meas = interp1d(frequencies_Meas, np.angle(Meas_fft))

    # initialize Hneu
    Hneu = transfer_function(Halt.f)

    # calculate Hneu in complex representation
    Umeas_div_Uid = magnitude_Meas(Halt.f) / magnitude_Ideal(Halt.f) * np.exp( 1j * (angle_Meas(Halt.f) - angle_Ideal(Halt.f) ) )
    Hneu.c = Halt.c * (1 + sigma_H * (Umeas_div_Uid - 1))



    return(Hneu)
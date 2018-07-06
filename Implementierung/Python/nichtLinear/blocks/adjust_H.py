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

    # if verbosity:
    #     delta_t_meas = (Uout_measured[1,0] - Uout_measured[0,0])
    #     delta_t_id = (Uout_ideal[1,0] - Uout_ideal[0,0])
    #     print('Zeitstep Meas: ' + str(delta_t_meas) +  ' Zeitstep Ideal: ' + str(delta_t_id) )
    #     fig = plt.figure()
    #     # Plot Spannungen
    #     plt.plot(Uout_ideal[:, 0], Uout_ideal[:, 1], 'r', Uout_measured[:, 0], Uout_measured[:, 1], 'b')
    #     plt.title('Uout_ideal - rot, Uout_meas - blau')
    #     plt.xlabel('t')
    #     plt.ylabel('U')
    #     plt.show()

    # find max Frequencies (Nyquists theorem):
    idx_half_Id = int(np.floor(len(Ideal_fft)/2))
    idx_half_Meas = int(np.floor(len(Meas_fft) / 2))
    f_max_Id = frequencies_Id[idx_half_Id]
    f_max_Meas = frequencies_Meas[idx_half_Meas]
    fmax_to_use = np.minimum(f_max_Id, f_max_Meas)
    idx_max_Id = np.array(np.where(frequencies_Id <= fmax_to_use))[0, -1]
    idx_max_Meas = np.array(np.where(frequencies_Meas <= fmax_to_use))[0, -1]
    # cut frequencies and FFTs to new Range -> only relevant frequencies ocurring
    frequencies_Id = frequencies_Id[0:idx_max_Id]
    frequencies_Meas = frequencies_Meas[0:idx_max_Meas]
    Ideal_fft = Ideal_fft[0:idx_max_Id]
    Meas_fft = Meas_fft[0:idx_max_Meas]
    
    # check frequency range of signal. If less frequencies than in H,
    # add frequency in signal with amplitude 1 s.t. signal has frequencies >= H
    # (factor is just what you like, calculated to enable Plots showing senseful scale)
    #factor = np.minimum(np.minimum(abs(Ideal_fft)), np.minimum(abs(Meas_fft)))
    factor = 1e-4
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

    # attempt 6.7. : calculate for amplitude and angle with similar formula:
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
        plt.title('Absratio Umeas / Uideal')
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
import numpy as np
import matplotlib.pyplot as plt
from helpers import csv_helper
import settings
from classes.signal_class import signal_class


def generate_BBsignal(f_rep=900e3, f_BB=5e6, Vpp=3, sample_rate_AWG_max=999900000, saveCSV=0, verbosity=0):
    """
     The method constructs a perfect signle-sinus as needed for the Barrier-Bucket-Applications
     with the given parameters

    :param f_rep: frequency of repetition of the WHOLE BB-signal, positive scalar
    :param f_BB: frequency of single-sinus, positive scalar with f_BB > f_rep
    :param Vpp: peak-to-peak Voltage of the signal, twice the amplitude of the single-sinus, positive scalar
    :param sample_rate_AWG_max: the maximum of the sample-rate of the AWG used to send signals, positive scalar
    :param saveCSV: flag, if CSV-data of the signal is desired, boolean
    :param verbosity: flag, if plot of the signal is desired, boolean


    :return: the BB-signal as instance of signal_class
    """


    a = sample_rate_AWG_max / f_rep

    num_points_rep = int(np.floor(sample_rate_AWG_max / f_rep))

    if num_points_rep % 2 == 0 :
        num_points_rep -= 1

    # T_BB = 1 / f_BB
    # T_rep = 1 / f_rep
    num_points_BB = num_points_rep / f_BB * f_rep

    num_points_BB = int(np.floor(num_points_BB))
    if num_points_BB % 2 == 0 :
        num_points_BB += 1



    sr = ( (num_points_rep - 1 ) * f_rep )
    t0 = 1 / sr

    T_rep = ( num_points_rep - 1 ) * t0

    T_BB = 1 / f_BB
    # t0 = (T_rep/(num_points_rep - 1))
    num_points_BB = int(np.floor(T_BB / t0))
    T_BB = t0 * (num_points_BB - 1 )

    t_BB = np.linspace(0, T_BB, num_points_BB)
    t_rep = np.linspace(0, T_rep, num_points_rep)

    U1 = np.sin(2 * np.pi * f_BB * t_BB)

    Uout = np.zeros([2, num_points_rep ])
    Uout[0,:] = t_rep;

    half1 = int(num_points_BB/2)
    mid2 = int((num_points_rep - 1) / 2)

    Uout[1,mid2-half1:mid2+half1+1] = Vpp / 2 * U1

    Uout = np.transpose(Uout)

    if verbosity :
        fig = plt.figure()
        plt.plot(t_rep, Uout[:,1])
        plt.title('Das ideale U_BB')
        plt.ylabel('u in mV')
        if settings.show_plots :
            plt.show()
#        fig.savefig('../../../ErstellteDokumente/Zwischenpraesentation/slides/ResultCode/plots/U_ideal.csv.csv.csv.csv.pdf')

    if saveCSV :

        csv_helper.save_2cols(settings.project_path + '/data/current_data/BBsignal_ideal.csv', Uout[0, :], Uout[1, :])

    Uout = signal_class(Uout[:, 0], Uout[:, 1])

    return Uout

def generate_BBsignal_new(f_rep=900e3, f_BB=5e6, Vpp=3, sample_rate_AWG_max=999900000, saveCSV=0, verbosity=0):
    """
     The method constructs a perfect signle-sinus as needed for the Barrier-Bucket-Applications
     with the given parameters

    :param f_rep: frequency of repetition of the WHOLE BB-signal, positive scalar
    :param f_BB: frequency of single-sinus, positive scalar with f_BB > f_rep
    :param Vpp: peak-to-peak Voltage of the signal, twice the amplitude of the single-sinus, positive scalar
    :param sample_rate_AWG_max: the maximum of the sample-rate of the AWG used to send signals, positive scalar
    :param saveCSV: flag, if CSV-data of the signal is desired, boolean
    :param verbosity: flag, if plot of the signal is desired, boolean


    :return: the BB-signal as instance of signal_class
    """


    num_points_rep = int(np.floor(sample_rate_AWG_max / f_rep))

    if num_points_rep % 2 == 0 :
        num_points_rep -= 1

    num_points_BB = num_points_rep / f_BB * f_rep
    num_points_BB = int(np.floor(num_points_BB))
    if num_points_BB % 2 == 0:
        num_points_BB += 1      # warum plus?



    real_SampleRate = ( num_points_rep * f_rep )
    delta_t = 1 / real_SampleRate

    t_max = ( num_points_rep - 1 ) * delta_t    #hoechster auftretender Wert

    t_maxBB = delta_t * (num_points_BB - 1 )

    t_BB = np.linspace(0, t_maxBB, num_points_BB)
    t_rep = np.linspace(0, t_max, num_points_rep)

    U1 = np.sin(2 * np.pi * f_BB * t_BB)

    Uout = np.zeros([2, num_points_rep ])
    Uout[0,:] = t_rep;

    half1 = int(num_points_BB/2)
    mid2 = int((num_points_rep - 1) / 2)

    Uout[1,mid2-half1:mid2+half1+1] = Vpp / 2 * U1

    Uout = np.transpose(Uout)

    if saveCSV:
        csv_helper.save_2cols(settings.project_path + '/data/current_data/BBsignal_new.csv', Uout[0, :], Uout[1, :])

    Uout = signal_class.gen_signal_from_sample_rate(Uout[:, 0], Uout[:, 1])

    return Uout

import numpy as np
import matplotlib.pyplot as plt
from helpers import csvHelper
import global_data
from classes.signal_class import signal_class


def generate_BBsignal(f_rep=900e3, f_BB=5e6, Vpp=3, sample_rate_AWG_max=999900000, saveCSV=0, verbosity=0):

    """
    generate_BBsignal generiert ein ideales Barrie-Bucket-Signal nach den Vorgaben f_rep, f_BB, Vpp

    INPUT:

        f_rep - positive integer; Wiederhohlfrequenz
        f_BB - positive integer; Barrier-Bucket-Frequenz
        Vpp - positive integer; Spitze-zu-Spitze - Spannung
        samplerateAWG - positive integer; Abtastarte des AWG

        saveCSV - boolean; ob Uout gespreichert werden soll
        verbosity - boolean; ob Uin gelplottet werden soll

    OUTPUT:

        Uout - nx2 array; Barrie-Bucket-Signal
            Uout[:,0] - Zeitvektor
            Uout[:,1] - Signalvektor

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
    num_points_BB = np.floor(T_BB / t0)
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
        if global_data.show_plots :
            plt.show()
#        fig.savefig('../../../ErstellteDokumente/Zwischenpraesentation/slides/ResultCode/plots/Uout_ideal.pdf')

    if saveCSV :

        csvHelper.save_2cols(global_data.project_path + '/data/current_data/BBsignal_ideal.csv', Uout[0, :], Uout[1, :])

    Uout = signal_class.gen_signal_from_old_convention(Uout[:,0], Uout[:,1])

    return Uout



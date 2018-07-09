from blocks.generate_BBsignal import generate_BBsignal
from blocks.compute_Uquest_from_Uout import compute_Uquest_from_Uout
from blocks.compute_K_from_a import compute_K_from_a
from blocks.compute_Uin_from_Uquest import compute_Uin_from_Uquest
from blocks.compute_a_from_Uin_Uquet import compute_a_from_Uin_Uquet
from blocks.measure_H import measure_H
from blocks.measure_Uout import measure_Uout
from helpers.signalHelper import convert_V_to_mV
from helpers.signalHelper import convert_mV_to_V
from helpers.signalHelper import setVpp
from helpers.csvHelper import read_in_transfer_function, read_in_transfer_function_old_convention
from global_data import project_path
from classes.signal_class import signal_class
from copy import copy
from helpers.csvHelper import save_2cols
from global_data import use_mock_system
from classes.signal_class import signal_class
from helpers.csvHelper import save_signale, save_transfer_function, save_transfer_function_old_convention
from blocks.adjust_H import adjust_H
from numpy import genfromtxt
import matplotlib.pyplot as plt
from global_data import project_path


import numpy as np


def evaluate_with_BBsignal_adjust_H(num_iters = 1) :

    if use_mock_system :
        data_directory = project_path + 'tools/adjustH/'
    else :
        data_directory = 'tests/mock_data/mock_results/'

    f_rep = 900e3
    f_BB = 5e6
    Vpp = 0.3

    sample_rate_AWG_max = 2e8
    sample_rate_DSO = 9999e5

    # f_rep = 2
    # f_BB = 4
    # sample_rate_AWG_max = 20

    Uout_ideal = generate_BBsignal(f_rep=f_rep, f_BB=f_BB, Vpp=Vpp, sample_rate_AWG_max=sample_rate_AWG_max, verbosity=0)

    H = measure_H()

    # save initial H

    save_transfer_function_old_convention(H=H, filename_a=data_directory + 'Ha_0.csv', filename_p= data_directory + 'Hp_0.csv')

    # a = determine_a(H, Uout_ideal, f_rep, Uout_ideal.sample_rate)

    a = determine_a(H, Uout_ideal, sample_rate_DSO, data_directory, f_rep)

    K = compute_K_from_a(a=a, verbosity=0)

    Uquest_ideal = compute_Uquest_from_Uout(Uout=Uout_ideal, H=H, verbosity=0)

    Uin = compute_Uin_from_Uquest(Uquest=Uquest_ideal, K=K, verbosity=0)

    Uin_measured, Uout_measured = measure_Uout(Uin=Uin, sample_rate_DSO=sample_rate_DSO )

    for i in range(1, num_iters+1):
        id = str(i)
        # compute new Uin
        Uquest_ideal = compute_Uquest_from_Uout(Uout=Uout_ideal, H=H, verbosity=0)

        Uin = compute_Uin_from_Uquest(Uquest=Uquest_ideal, K=K, verbosity=0)

        Uin_measured, Uout_measured = measure_Uout(Uin=Uin, sample_rate_DSO=sample_rate_DSO )

        # begin cut just one period out of Uout_measured

        Uout_ideal = Uout_ideal.cut_one_period(f_rep)
        Uout_measured = Uout_measured.cut_one_period ( f_rep )
        Uin_measured = Uin_measured.cut_one_period( f_rep )

        # save Uin and Uout
        save_signale(Uin_measured, data_directory + 'Uin_' + id + '.csv')
        save_signale(Uout_measured, data_directory + 'Uout_' + id + '.csv')

        if use_mock_system != 1:
            save_2cols('tools/csvDateien_K/Uout_' + id + '.csv', Uout_measured[:, 0], Uout_measured[:, 1])

        # quality = evaluate_signal('tools/csvDateien_K/Uout_' + id + '.csv', 'csvDateien_K/results_adjust_H.csv')
        sigma_H = 0.5

        H = adjust_H(H, Uout_ideal, Uout_measured, sigma_H=sigma_H, verbosity=0)

        save_transfer_function_old_convention(H, data_directory + 'Ha_' + id + '.csv', data_directory + 'Hp_' + id + '.csv')

        plot_H_0_H_current(H, id, data_directory)

    # quality = test_evaluate()

    plot_H_1_H_0(data_directory)

    H_0 = read_in_transfer_function_old_convention(data_directory + 'Ha_0.csv', data_directory + 'Hp_0.csv')

    return Uout_ideal, Uout_measured, H_0, H


def plot_H_0_H_current(H, id, data_directory):
    verbosity = 0
    if verbosity:
        H_0 = read_in_transfer_function_old_convention(data_directory + 'Ha_0.csv', data_directory + 'Hp_0.csv')
        plt.figure(1)
        plt.plot(H_0.f, H_0.a, 'r', H.f, H.a, 'b')
        plt.title('Runde 0 - rot, Runde ' + id + ' - blau')
        plt.xlabel('f')
        plt.ylabel('Ha')
        plt.show()


def plot_H_1_H_0(data_directory):
    verbosity = 0
    if verbosity:
        Ha_0 = genfromtxt(data_directory + 'Ha_0.csv', delimiter=',')
        Ha_1 = genfromtxt(data_directory + 'Ha_1.csv', delimiter=',')

        plt.figure(1)
        plt.plot(Ha_0[:, 0], Ha_0[:, 1], 'r', Ha_1[:, 0], Ha_1[:, 1], 'b')
        plt.title('Runde 1 - rot, Runde 3 - blau')
        plt.xlabel('f')
        plt.ylabel('Ha')
        plt.show()

        if use_mock_system != 1:
            Uout_measured1 = genfromtxt('tools/csvDateien_K/Uout_1.csv', delimiter=',')
            Uout_measured10 = genfromtxt('tools/csvDateien_K/Uout_3.csv', delimiter=',')
        plt.figure(1)
        plt.plot(Uout_measured1[:, 0], Uout_measured1[:, 1], 'r', Uout_measured10[:, 0], Uout_measured10[:, 1], 'b')
        plt.title('Runde 1 - rot, Runde 3 - blau')
        plt.xlabel('t')
        plt.ylabel('U')
        plt.show()


def determine_a(H, Uout_ideal, sample_rate_DSO, data_directory, f_rep):
    Uquest_ideal = compute_Uquest_from_Uout(Uout=Uout_ideal, H=H, verbosity=0)
    Uin = copy(Uquest_ideal)
    Uin.Vpp = 0.3
    Uin_measured, Uout_measured = measure_Uout(Uin=Uin, sample_rate_DSO=sample_rate_DSO, loadCSV=0, saveCSV=0, id='1',
                                               verbosity=0)
    # save initial Data
    save_2cols(data_directory + 'Uin_0.csv', Uin_measured.time, Uin_measured.in_V)
    save_2cols(data_directory + 'Uout_0.csv', Uout_measured.time, Uout_measured.in_V)

    Uout_measured = Uout_measured.cut_one_period(f_rep)
    Uquest_measured = compute_Uquest_from_Uout(Uout=Uout_measured, H=H, verbosity=0)
    a = compute_a_from_Uin_Uquet(Uin=Uin, Uquest=Uquest_measured, N=3)
    return a



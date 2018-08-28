from blocks.generate_BBsignal import generate_BBsignal
from blocks.compute_Uquest_from_Uout import compute_Uquest_from_Uout
from blocks.compute_K_from_a import compute_K_from_a
from blocks.compute_Uin_from_Uquest import compute_Uin_from_Uquest
from blocks.compute_a_from_Uin_Uquet import compute_a_from_Uin_Uquet
from blocks.determine_H import determine_H
from blocks.measure_Uout import measure_Uout
from helpers.signal_helper import convert_V_to_mV
from helpers.signal_helper import convert_mV_to_V
from helpers.signal_helper import setVpp
from helpers.csv_helper import save_transfer_function, save_2cols, save_signal, save_a
from settings import project_path
from classes.signal_class import signal_class
from copy import copy
from blocks.determine_a import determine_a
from save_results import save, save_text
from settings import use_mock_system, f_rep, f_BB, sample_rate_AWG_max, sample_rate_DSO, get_H_K_Vpp, get_H_K_KVpp, add_final_comment, get_H_K_save_to_csv

import numpy as np


def evaluate_with_BBsignal(num_iters = 1) :

    if use_mock_system :

        data_directory = project_path + 'tests/mock_data/mock_results/get_H_K/'

    else :

        data_directory = project_path + save(path='data/get_blocks', name='measure_H_K') + '/'


    Vpp = get_H_K_Vpp
    Vpp_K = get_H_K_KVpp

    Uout_ideal = generate_BBsignal(f_rep=f_rep, f_BB=f_BB, Vpp=Vpp, sample_rate_AWG_max=sample_rate_AWG_max, verbosity=0)
    Uout_ideal_for_K = generate_BBsignal(f_rep=f_rep, f_BB=f_BB, Vpp=Vpp_K,
                                         sample_rate_AWG_max=sample_rate_AWG_max,
                                         verbosity=0)

    H = determine_H(loadCSV=0, saveCSV=0, verbosity=0)
    a = determine_a(H, Uout_ideal_for_K, sample_rate_DSO, data_directory=data_directory)

    K = compute_K_from_a(a=a, verbosity=0)

    Uquest_ideal = compute_Uquest_from_Uout(Uout=Uout_ideal, H=H, verbosity=0)

    Uin, Uquest_ideal = compute_Uin_from_Uquest(Uquest=Uquest_ideal, K_Uin_to_Uquest=K, verbosity=0)

    Uin_measured, Uout_measured = measure_Uout(Uin=Uin, sample_rate_DSO=sample_rate_DSO, verbosity=0)

    save_transfer_function(H=H, filename=data_directory + 'H.csv')

    if get_H_K_save_to_csv[0] or get_H_K_save_to_csv[1]:
        save_transfer_function(H=H, filename=data_directory + 'H.csv')

    if get_H_K_save_to_csv[0] or get_H_K_save_to_csv[2]:
        save_a(a, filename=data_directory + '/a.csv')

    if get_H_K_save_to_csv[0] or get_H_K_save_to_csv[3]:
        save_2cols(data_directory + '/K_initial.csv', K[:, 0], K[:, 1])

    if get_H_K_save_to_csv[0] or get_H_K_save_to_csv[4]:
        save_signal(Uin_measured, data_directory + 'Uin_measured.csv')
        save_signal(Uquest_ideal, data_directory + 'Uquest_ideal.csv')
        save_signal(Uout_measured, data_directory + 'Uout_measured.csv')

    if (not use_mock_system) and add_final_comment:
        save_text(data_directory)


    return Uout_ideal, Uout_measured
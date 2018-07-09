from blocks.generate_BBsignal import generate_BBsignal
from blocks.compute_Uquest_from_Uout import compute_Uquest_from_Uout
from blocks.compute_K_from_a import compute_K_from_a
from blocks.compute_Uin_from_Uquest import compute_Uin_from_Uquest
from blocks.compute_a_from_Uin_Uquet import compute_a_from_Uin_Uquet
from blocks.measure_H import measure_H
from blocks.measure_Uout import measure_Uout
from helpers.signal_helper import convert_V_to_mV
from helpers.signal_helper import convert_mV_to_V
from helpers.signal_helper import setVpp
from helpers.csv_helper import read_in_transfer_function, read_in_transfer_function_old_convention
from global_data import project_path
from classes.signal_class import signal_class
from copy import copy
from helpers.csv_helper import save_2cols
from global_data import use_mock_system
from classes.signal_class import signal_class
from helpers.csv_helper import save_signale, save_transfer_function_old_convention
from blocks.adjust_H import adjust_H
from numpy import genfromtxt
import matplotlib.pyplot as plt
from global_data import project_path
from blocks.loop_adjust_H import loop_adjust_H
from blocks.determine_a import determine_a


import numpy as np


def evaluate_adjust_H(num_iters = 1) :

    if use_mock_system :
        data_directory = project_path + 'tests/mock_data/mock_results/adjust_H/'
    else :
        data_directory = project_path + 'tools/adjustH/'


    f_rep = 900e3
    f_BB = 5e6
    Vpp = 0.3

    sample_rate_AWG_max = 2e8
    sample_rate_DSO = 9999e5

    Uout_ideal = generate_BBsignal(f_rep=f_rep, f_BB=f_BB, Vpp=Vpp, sample_rate_AWG_max=sample_rate_AWG_max)

    H = measure_H()

    save_transfer_function_old_convention(H=H, directory=data_directory, id = '0' )

    a = determine_a(H, Uout_ideal, sample_rate_DSO, data_directory)
    K = compute_K_from_a(a=a, verbosity=0)

    H, Uout_measured = loop_adjust_H(H, K, Uout_ideal, data_directory, num_iters, sample_rate_DSO)

    H_0 = read_in_transfer_function_old_convention(data_directory + 'Ha_0.csv', data_directory + 'Hp_0.csv')

    return Uout_ideal, Uout_measured, H_0, H
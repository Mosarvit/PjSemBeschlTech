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
from settings import project_path
from classes.signal_class import signal_class
from copy import copy
from helpers.csv_helper import save_2cols
from settings import use_mock_system
from classes.signal_class import signal_class
from helpers.csv_helper import save_signale, save_transfer_function
from blocks.adjust_H import adjust_H
from numpy import genfromtxt
import matplotlib.pyplot as plt
from settings import project_path
from blocks.determine_a import determine_a
from helpers.plot_helper import plot_2_transfer_functions
from blocks.generate_BBsignal import generate_BBsignal
from settings import verbosity

def loop_adjust_H(H, K, Uout_ideal, data_directory, num_iters, sample_rate_DSO, low_amplitude=0, verbosity=0):

    for i in range(1, num_iters + 1):
        id = str(i)
        # compute new Uin
        Uquest = compute_Uquest_from_Uout(Uout=Uout_ideal, H=H)

        if low_amplitude :
            Uin = Uquest
        else :
            Uin = compute_Uin_from_Uquest(Uquest=Uquest, K=K)

        Uin_measured, Uout_measured = measure_Uout(Uin=Uin, sample_rate_DSO=sample_rate_DSO)

        f_rep_fix = 9e5     
        Uout_measured = Uout_measured.cut_one_period(f_rep_fix)
        Uin_measured = Uin_measured.cut_one_period(f_rep_fix)
#        Uout_measured = Uout_measured.cut_one_period(Uin.f_rep)
#        Uin_measured = Uin_measured.cut_one_period(Uin.f_rep)

        # save Uin and Uout
        save_signale(Uin_measured, data_directory + 'Uin_' + id + '.csv')
        save_signale(Uout_measured, data_directory + 'Uout_' + id + '.csv')

#        if use_mock_system != 1:
#            save_2cols('tools/csvDateien_K/Uout_' + id + '.csv', Uout_measured.time, Uout_measured.in_mV)

        # quality = evaluate_signal('tools/csvDateien_K/Uout_' + id + '.csv', 'csvDateien_K/results_adjust_H.csv')
        # first try gsi
        sigma_H = 0.1
        sample_rate_DSO = 9999e5
        f_rep = 900e3
        f_BB = 5e6
        Vpp = 0.6
        Uout_ideal_for_FFT = generate_BBsignal(f_rep=f_rep, f_BB=f_BB, Vpp=Vpp, sample_rate_AWG_max=sample_rate_DSO)

        H = adjust_H(H, Uout_ideal_for_FFT, Uout_measured, sigma_H=sigma_H, verbosity=verbosity)

        save_transfer_function(H, directory=data_directory, id=id)
        
        plot_H_0_H_current(H, id, data_directory)

    return H, Uout_measured

def plot_H_0_H_current(H, id, data_directory):
    verbosity = 0
    if verbosity:
        H_0 = read_in_transfer_function_old_convention(data_directory + 'Ha_0.csv', data_directory + 'Hp_0.csv')
        plot_2_transfer_functions(H1=H_0, H2=H, legend1='H_0', legend2='H_' + id)
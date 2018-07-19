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
from blocks.adjust_a import adjust_a
from numpy import genfromtxt
import matplotlib.pyplot as plt
from settings import project_path
from blocks.determine_a import determine_a
from helpers.plot_helper import plot_2_transfer_functions, plot_2_signals

from helpers.signal_evaluation import signal_evaluate

def loop_adjust_a(a, K_0, H, Uout_ideal, data_directory, num_iters, sample_rate_DSO):
    quality_development = []
    #Initialisierung
    K = K_0
    for i in range(1, num_iters + 1):
        # in welchem Bereich a angepasst wird
        
        Vpp = 0.6
        id = str(i)

        # compute new Uin
        Uout_ideal.Vpp = 1.5
        Uquest_ideal = compute_Uquest_from_Uout(Uout=Uout_ideal, H=H)
        save_signale(Uquest_ideal, data_directory + 'Uquest_ideal_' + id + '.csv')
        Uin = compute_Uin_from_Uquest(Uquest=Uquest_ideal, K=K)
        Uin_measured, Uout_measured = measure_Uout(Uin=Uin, sample_rate_DSO=sample_rate_DSO)
        
        save_signale(Uin_measured, data_directory + 'Uin_measured_uncut_' + id + '.csv')
        save_signale(Uout_measured, data_directory + 'Uout_measured_uncut_' + id + '.csv')
        
        plot_2_signals(Uin_measured, Uout_measured, 'Uin_measured_uncut', 'Uout_measured_uncut')
        
        f_rep_fix = 9e5     
        Uout_measured = Uout_measured.cut_one_period(f_rep_fix)
        Uin_measured = Uin_measured.cut_one_period(f_rep_fix)

        # save Uin and Uout
        save_signale(Uin, data_directory + 'Uin_awg_' + id + '.csv')
        save_signale(Uquest_ideal, data_directory + 'Uquest_' + id + '.csv')
        save_signale(Uin_measured, data_directory + 'Uin_measured_' + id + '.csv')
        save_signale(Uout_measured, data_directory + 'Uout_measured_' + id + '.csv')
        
        plot_2_signals(Uin_measured, Uout_measured, 'Uin_measured', 'Uout_measured')
        

        quality = signal_evaluate(data_directory + 'Uout_measured_' + id + '.csv', data_directory + 'quality_' + id + '.csv')
        quality_development.append(quality)

        sigma_a = 0.5
        Uquest_measured = compute_Uquest_from_Uout(Uout=Uout_measured, H=H)
        a_new = adjust_a(a, Uin, Uquest_ideal, Uquest_measured, sigma_a)
        K = compute_K_from_a(a=a_new, verbosity=1)
        save_2cols(data_directory + '/K_'+ id +'.csv', K[:, 0], K[:, 1])
        
        plot_a_0_a_current(K_0, K, id)

    print('quality_development' + str(quality_development))
    return K, Uout_measured, quality_development

def plot_a_0_a_current(K_0, K, id):
    verbosity = 1
    if verbosity:
        plt.figure()
        plt.plot(K_0[:,0], K_0[:,1])
        plt.plot(K[:,0], K[:,1])
        plt.legend(['K_0', 'K_' + id])
        plt.xlabel('Uin')
        plt.ylabel('Uquest')
        plt.show()
from blocks.compute_Uin_from_Uquest import compute_Uin_from_Uquest
from blocks.compute_Uquest_from_Uout import compute_Uquest_from_Uout
from blocks.measure_Uout import measure_Uout
from helpers.csv_helper import save_2cols
from helpers.csv_helper import save_signal
from helpers.plot_helper import plot_2_signals
from helpers.signal_evaluation import signal_evaluate
from blocks.adjust_a import adjust_a
from blocks.compute_K_from_a import compute_K_from_a


def loop_adjust_a(a, K_0, H, Uout_ideal, data_directory, num_iters, sample_rate_DSO):
    quality_development = []
    #Initialisierung
    K = K_0
    Ks = []
    Ks.append(K_0)
    for i in range(1, num_iters + 1):
        # in welchem Bereich a angepasst wird
        
        Vpp = 0.6
        id = str(i)

        # compute new Uin
        Uout_ideal.Vpp = 6
        Uquest_ideal = compute_Uquest_from_Uout(Uout=Uout_ideal, H=H)
        save_signal(Uquest_ideal, data_directory + 'Uquest_ideal_' + id + '.csv')
        Uin = compute_Uin_from_Uquest(Uquest=Uquest_ideal, K_Uin_to_Uquest=K)
        Uin_measured, Uout_measured = measure_Uout(Uin=Uin, sample_rate_DSO=sample_rate_DSO)
        
        save_signal(Uin_measured, data_directory + 'Uin_measured_uncut_' + id + '.csv')
        save_signal(Uout_measured, data_directory + 'Uout_measured_uncut_' + id + '.csv')
        
        # plot_2_signals(Uin_measured, Uout_measured, 'Uin_measured_uncut', 'Uout_measured_uncut')
        
        f_rep_fix = 9e5     
        Uout_measured = Uout_measured.cut_one_period(f_rep_fix)
        Uin_measured = Uin_measured.cut_one_period(f_rep_fix)

        # save Uin and Uout
        save_signal(Uin, data_directory + 'Uin_awg_' + id + '.csv')
        save_signal(Uquest_ideal, data_directory + 'Uquest_' + id + '.csv')
        save_signal(Uin_measured, data_directory + 'Uin_measured_' + id + '.csv')
        save_signal(Uout_measured, data_directory + 'Uout_measured_' + id + '.csv')
        
        # plot_2_signals(Uin_measured, Uout_measured, 'Uin_measured', 'Uout_measured')
        

        quality = signal_evaluate(data_directory + 'Uout_measured_' + id + '.csv', data_directory + 'quality_' + id + '.csv')
        quality_development.append(quality)

        sigma_a = 0.5
        Uquest_measured = compute_Uquest_from_Uout(Uout=Uout_measured, H=H)
        a_new = adjust_a(a, Uin, Uquest_ideal, Uquest_measured, sigma_a)
        K = compute_K_from_a(a=a_new, verbosity=0)
        Ks.append(K)
        save_2cols(data_directory + '/K_'+ id +'.csv', K[:, 0], K[:, 1])


    print('quality_development' + str(quality_development))
    return K, Uout_measured, quality_development, Ks


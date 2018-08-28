from blocks.compute_Uin_from_Uquest import compute_Uin_from_Uquest
from blocks.compute_Uquest_from_Uout import compute_Uquest_from_Uout
from blocks.measure_Uout import measure_Uout
from helpers.csv_helper import save_signal, save_a, save_K
from helpers.signal_evaluation import signal_evaluate
from blocks.adjust_a import adjust_a
from blocks.compute_K_from_a import compute_K_from_a
from settings import f_rep, adjust_K_Vpp, sigma_a, adjust_a_save_to_csv


def loop_adjust_a(a, K_0, H, Uout_ideal, data_directory, num_iters, sample_rate_DSO):
    quality_development = []
    #Initialisierung
    K = K_0
    Ks = []
    Ks.append(K_0)
    for i in range(1, num_iters + 1):
        # in welchem Bereich a angepasst wird

        id = str(i)

        # compute new Uin
        Uout_ideal.Vpp = adjust_K_Vpp
        Uquest_ideal = compute_Uquest_from_Uout(Uout=Uout_ideal, H=H)

#        Uquest_ideal.Vpp = 0.2
        Uin, Uquest_adapted = compute_Uin_from_Uquest(Uquest=Uquest_ideal, K_Uin_to_Uquest=K, verbosity = 0)
        Uin_measured, Uout_measured = measure_Uout(Uin=Uin, sample_rate_DSO=sample_rate_DSO)

        if adjust_a_save_to_csv[0] or adjust_a_save_to_csv[4]:
            save_signal(Uin_measured, data_directory + 'Uin_measured_uncut_' + id + '.csv')
            save_signal(Uout_measured, data_directory + 'Uout_measured_uncut_' + id + '.csv')
        
        # plot_2_signals(Uin_measured, Uout_measured, 'Uin_measured_uncut', 'Uout_measured_uncut')

        Uout_measured = Uout_measured.cut_one_period(f_rep)
        Uin_measured = Uin_measured.cut_one_period(f_rep)

        # save Uin and Uout
        if adjust_a_save_to_csv[0] or adjust_a_save_to_csv[5]:
            save_signal(Uin, data_directory + 'Uin_ideal_' + id + '.csv')
            save_signal(Uin_measured, data_directory + 'Uin_measured_' + id + '.csv')
            save_signal(Uout_measured, data_directory + 'Uout_measured_' + id + '.csv')
            save_signal(Uquest_adapted, data_directory + 'Uquest_adapted_' + id + '.csv')
            save_signal(Uquest_ideal, data_directory + 'Uquest_ideal_' + id + '.csv')

        # plot_2_signals(Uin_measured, Uout_measured, 'Uin_measured', 'Uout_measured')

        # taken out because of causing recursion error
        quality = signal_evaluate(data_directory + 'Uout_measured_' + id + '.csv', data_directory + 'quality_' + id + '.csv')
        # quality = 5
        quality_development.append(quality)

        Uquest_measured = compute_Uquest_from_Uout(Uout=Uout_measured, H=H)
        a_new = adjust_a(a, Uin, Uquest_adapted, Uquest_measured, sigma_a)
        K = compute_K_from_a(a=a_new, verbosity=0)
        Ks.append(K)

        if adjust_a_save_to_csv[0] or adjust_a_save_to_csv[6]:
            save_K(K, data_directory + '/K_' + id + '.csv')
            save_a(a_new, data_directory + 'a_' + id + '.csv')

    print('quality_development' + str(quality_development))
    return Uout_measured, quality_development, Ks


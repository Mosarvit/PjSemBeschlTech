from blocks.compute_K_from_a import compute_K_from_a
from blocks.determine_a import determine_a
from blocks.generate_BBsignal import generate_BBsignal
from blocks.loop_adjust_a import loop_adjust_a
from blocks.determine_H import determine_H
from helpers.csv_helper import save_2cols
from helpers.csv_helper import save_transfer_function, save_signal, save_a
from helpers.plot_helper import plot_Ks
from helpers.save_results import save, save_text
from settings import project_path, use_mock_system, adjust_a_save_to_csv
import settings

def evaluate_adjust_a(num_iters = 1, verbosity = 0) :
    '''
    This routine handles the adjustment of a on a meta-level. It sets the setup and starts the iterative adjustment.
    :param num_iters: integer, number of steps to execute
    :param verbosity: boolean, whether to show plots
    :return: ideal output signal, last measured signal, list of nonlinearity Ks from the steps
    '''

    if use_mock_system:
        data_directory = project_path + 'tests/mock_data/mock_results/adjust_a/'
    else:
        data_directory = project_path + save(path='data/optimizer', name='adjust_a') + '/'


    f_rep = settings.f_rep
    f_BB = settings.f_BB
    Vpp = settings.adjust_K_Vpp

    sample_rate_AWG_max = settings.sample_rate_AWG_max
    sample_rate_DSO = settings.sample_rate_DSO

    Uout_ideal = generate_BBsignal(f_rep=f_rep, f_BB=f_BB, Vpp=Vpp, sample_rate_AWG_max=sample_rate_AWG_max)

    save_signal(Uout_ideal, data_directory+'Uout_ideal.csv')

    H_0 = determine_H(loadCSV=0, saveCSV=0)
    if adjust_a_save_to_csv[0] or adjust_a_save_to_csv[1]:
        save_transfer_function(H=H_0, filename=data_directory + 'H_initial.csv')

    a_0 = determine_a(H_0, Uout_ideal, sample_rate_DSO, data_directory)

    if adjust_a_save_to_csv[0] or adjust_a_save_to_csv[2]:
        save_a(a_0, data_directory + 'a_initial.csv')

    K_0 = compute_K_from_a(a=a_0, verbosity=0)

    if adjust_a_save_to_csv[0] or adjust_a_save_to_csv[3]:
       save_2cols(data_directory + '/K_initial.csv', K_0[:, 0], K_0[:, 1])

    Uout_measured, quality_development, Ks = loop_adjust_a(a_0, K_0, H_0, Uout_ideal, data_directory, num_iters=num_iters, sample_rate_DSO=sample_rate_DSO)
    
    if verbosity or settings.show_final_adjustment:
        plot_Ks(Ks)
    if (not use_mock_system) and settings.add_final_comment :
        save_text(data_directory)

    return Uout_ideal, Uout_measured, Ks



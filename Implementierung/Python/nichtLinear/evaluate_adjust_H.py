from blocks.generate_BBsignal import generate_BBsignal
from blocks.compute_K_from_a import compute_K_from_a
from blocks.determine_H import determine_H
from helpers.csv_helper import save_2cols
from helpers.csv_helper import save_signal, save_transfer_function, read_in_transfer_function
from settings import use_mock_system, project_path, show_plot_final_adjustment_H ,f_rep, f_BB, add_final_comment, sample_rate_AWG_max,sample_rate_DSO, adjust_H_Vpp, adjust_H_save_to_csv
from blocks.loop_adjust_H import loop_adjust_H
from blocks.determine_a import determine_a
from helpers.plot_helper import plot_Hs
from helpers.save_results import save, save_text


def evaluate_adjust_H(num_iters = 1, verbosity = 0):
    '''
    This routine handles the iterative adjustment of H on a meta-level. It sets the setup and starts the iterative adjustment.

    :param num_iters: integer, number of steps to execute.
    :param verbosity: boolean, whether to show plots
    :return: desired output signal, last measured output signal
    '''

    if use_mock_system :

        data_directory = project_path + 'tests/mock_data/mock_results/adjust_H/'

    else :

        data_directory = project_path + save(path='data/optimizer', name='adjust_H') + '/'


    Vpp = adjust_H_Vpp

    Uout_ideal = generate_BBsignal(f_rep=f_rep, f_BB=f_BB, Vpp=Vpp, sample_rate_AWG_max=sample_rate_AWG_max, verbosity=0)


    H = determine_H(loadCSV=0, saveCSV=0, verbosity=0)

    if adjust_H_save_to_csv[0] or adjust_H_save_to_csv[1]:
        save_transfer_function(H=H, filename=data_directory + 'H_0.csv')
        save_signal(Uout_ideal, data_directory + 'Uout_ideal.csv')

    a = determine_a(H, Uout_ideal, sample_rate_DSO, data_directory)

    K = compute_K_from_a(a=a, verbosity=0)
    # plot_K(K)

    if adjust_H_save_to_csv[0] or adjust_H_save_to_csv[2]:
        save_2cols(data_directory + '/K_initial.csv', K[:, 0], K[:, 1])

    Hs, Uout_measured, quality_development = loop_adjust_H(H, K, Uout_ideal, data_directory, num_iters=num_iters, sample_rate_DSO=sample_rate_DSO)

    H_0 = read_in_transfer_function(data_directory + 'H_0.csv')
    if verbosity or show_plot_final_adjustment_H:
        plot_Hs(Hs)

    if (not use_mock_system) and add_final_comment :
        save_text(data_directory)

    return Uout_ideal, Uout_measured, Hs



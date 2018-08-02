from blocks.compute_K_from_a import compute_K_from_a
from blocks.determine_a import determine_a
from blocks.generate_BBsignal import generate_BBsignal
from blocks.loop_adjust_a import loop_adjust_a
from blocks.measure_H import measure_H
from helpers.csv_helper import save_2cols
from helpers.csv_helper import save_transfer_function
from save_results import save, save_text
from settings import project_path
from settings import use_mock_system


def evaluate_adjust_a(num_iters = 1, verbosity = 0) :

    if use_mock_system:
        data_directory = project_path + 'tests/mock_data/mock_results/adjust_a/'
    else:
        data_directory = project_path + save(path='data/optimizer', name='adjust_a') + '/'


    f_rep = 900e3
    f_BB = 5e6
    Vpp = 3

    sample_rate_AWG_max = 2e8
    sample_rate_DSO = 9999e5

    Uout_ideal = generate_BBsignal(f_rep=f_rep, f_BB=f_BB, Vpp=Vpp, sample_rate_AWG_max=sample_rate_AWG_max)

    H = measure_H(loadCSV=1, saveCSV=1)

    save_transfer_function(H=H, filename=data_directory + 'H_0')

    a_0 = determine_a(H, Uout_ideal, sample_rate_DSO, data_directory)

    K_0 = compute_K_from_a(a=a_0, verbosity=0)
    save_2cols(data_directory + '/K_initial.csv', K_0[:, 0], K_0[:, 1])

    K, Uout_measured, quality_development, Ks = loop_adjust_a(a_0, K_0, H, Uout_ideal, data_directory, num_iters=num_iters, sample_rate_DSO=sample_rate_DSO)

    if not use_mock_system :
        save_text(data_directory)

    return Uout_ideal, Uout_measured, Ks



from unittest import TestCase

from scipy import linalg

from evaluate_adjust_a import evaluate_adjust_a
from helpers.overlay import overlay
from helpers.plot_helper import plot_2_signals, plot_2_transfer_functions, plot_3_transfer_functions, plot_3_Ks, plot_K_ideal_Ks, plot_K
from helpers.signal_helper import calculate_error
from helpers.csv_helper import save_K, read_in_K
from settings import mock_system, project_path

data_directory = project_path + 'tests/mock_data/mock_results/adjust_a/'
K_mock = read_in_K(data_directory + 'K_mock.csv')
sq= 250
K_mock = K_mock[sq:997-sq, :]
save_K(K_mock, data_directory + 'K_mock_trimmed.csv')
plot_K(K_mock)

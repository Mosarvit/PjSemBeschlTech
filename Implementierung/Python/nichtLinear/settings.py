from tests.mock_system.mock_system_class import mock_system_class
import os

"""
This file contains parameters used in different methods. Use and manipulate before starting runme.
See manual.txt for further explanation
Date 29.08.2018
"""


# basic parameters
use_mock_system = 1
verbosity = 0
f_rep = 900e3
f_BB = 5e6
sample_rate_AWG_max = 2e8
sample_rate_DSO = 9999e5
max_input_vpp_amplifier = 1
add_final_comment = 1
polynomial_order = 3

# parameters just for returning H and K
get_H_K_Vpp = 0.3
get_H_K_KVpp = 0.6
get_H_K_save_to_csv = [
    1 , # save all data
    1 , # save H
    1 , # save exponents a
    1 , # save nonlinearity K
    1 , # save signals Uquest (ideal), Uin_measured, Uout_measured
]

# parameters for adjust H (iterative optimization of H)
number_iterations = 5
sigma_H = 0.5
adjust_H_Vpp = 0.3
adjust_H_Vpp_K = 0.6
adjust_H_save_to_csv = [
    1 , # save all data
    1 , # save initial H (measured)
    1 , # save K
    0 , # save measured but not reduced to one period input and output signals in every step
    1 , # save measured / calculated Uin, Uin_measured, Uquest, Uout_measured in every step
    1 , # save adapted H in every step
]
use_rms = False
ratio_of_rms_to_ignore = 0.02
use_zero_padding = False
ratio_to_cut = 3e-3
default_ratio_in_spectre = 3e-3
show_plots_in_adjust_H = False




# global parameters you should be sure you'd like to change
project_path = os.path.dirname(os.path.abspath(__file__)) + '/'
mock_data_path = project_path + 'tests/mock_data/'
test_data_path = mock_data_path + 'unit_test_data/'
get_H_data_path_real_system = project_path + '/data/get_H/'
get_H_data_path_mock = mock_data_path + '/mock_data/get_H/'
show_plots = 1 # ob die Plots angenzeigt werden sollen
mock_system = mock_system_class()
last_directory_used = '000'

def set_last_directory_used(value):
    global last_directory_used   # declare a to be a global
    last_directory_used = value


# default values of variables named above:
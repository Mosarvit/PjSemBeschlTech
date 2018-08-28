from tests.mock_system.mock_system_class import mock_system_class
import os

"""
Hier sind globale Variablen gespreicher. Eine Zwischelösung.
"""

project_path = os.path.dirname(os.path.abspath(__file__)) + '/'
mock_data_path = project_path + 'tests/mock_data/'
test_data_path = mock_data_path + 'unit_test_data/'
get_H_data_path_real_system = project_path + '/data/get_H/'
get_H_data_path_mock = mock_data_path + '/mock_data/get_H/'
show_plots = 1 # ob die Plots angenzeigt werden sollen
mock_system = mock_system_class()
use_mock_system = 1
verbosity = 0
last_directory_used = '000'

f_rep = 900e3
f_BB = 5e6
Vpp = 3

sample_rate_AWG = 2e8
sample_rate_DSO = 999900000

def set_last_directory_used(value):
    global last_directory_used   # declare a to be a global
    last_directory_used = value

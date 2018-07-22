from tests.mock_system.mock_system_class import mock_system_class
import os

"""
Hier sind globale Variablen gespreicher. Eine Zwischelösung.
"""

project_path = os.path.dirname(os.path.abspath(__file__)) + '/'
mock_data_path = project_path + '/tests/mock_data/'
get_H_data_path_measuraments = project_path + '/data/get_H/'
get_H_data_path_mock = mock_data_path + '/mock_data/get_H/'
show_plots = 1 # ob die Plots angenzeigt werden sollen
save_as_tikz = 1 # speichert plots
mock_system = mock_system_class()
use_mock_system = 1
verbosity = 0
last_directory_used = '000'

def set_last_directory_used(value):
    global last_directory_used   # declare a to be a global
    last_directory_used = value

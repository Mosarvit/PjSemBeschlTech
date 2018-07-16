from tests.mock_system.mock_system_class import mock_system_class
import os

"""
Hier sind globale Variablen gespreicher. Eine Zwischelösung.
"""

project_path = os.path.dirname(os.path.abspath(__file__)) + '/'
mock_data_directory = project_path + '/tests/mock_data/'
show_plots = 1 # ob die Plots angenzeigt werden sollen
mock_system = mock_system_class()
use_mock_system = 0

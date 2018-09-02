# -*- coding: utf-8 -*-

from blocks.generate_BBsignal import generate_BBsignal
from blocks.compute_Uquest_from_Uout import compute_Uquest_from_Uout
from blocks.compute_K_from_a import compute_K_from_a
from blocks.compute_Uin_from_Uquest import compute_Uin_from_Uquest
from blocks.compute_a_from_Uin_Uquest import compute_a_from_Uin_Uquest
from blocks.determine_H import determine_H
from blocks.measure_Uout import measure_Uout
from helpers.signal_helper import convert_V_to_mV
from helpers.signal_helper import convert_mV_to_V
from helpers.signal_helper import setVpp
from helpers.csv_helper import read_in_transfer_function, read_in_transfer_function_old_convention
from settings import project_path
from classes.signal_class import signal_class
from copy import copy
from helpers.csv_helper import save_2cols
from settings import use_mock_system
from classes.signal_class import signal_class
from helpers.csv_helper import save_signal, save_transfer_function
from blocks.adjust_H import adjust_H
from numpy import genfromtxt
import matplotlib.pyplot as plt
from settings import project_path
from blocks.determine_a import determine_a
from helpers.plot_helper import plot_2_transfer_functions, plot_2_signals
from settings import project_path
import numpy as np
 

H_0 = read_in_transfer_function(project_path + 'data\optimizer\\adjust_H_19_07_2018-10_58_39\H_0.csv')


for i in range(4):
    H_i = read_in_transfer_function(project_path + 'data\optimizer\\adjust_H_19_07_2018-10_58_39\H_'+str(i)+'.csv')
    plot_2_transfer_functions(H_0, H_i, '0', str(i))



from blocks.generate_BBsignal import generate_BBsignal
from blocks.compute_Uquest_from_Uout import compute_Uquest_from_Uout
from blocks.compute_K_from_a import compute_K_from_a
from blocks.compute_Uin_from_Uquest import compute_Uin_from_Uquest
from blocks.compute_a_from_Uin_Uquet import compute_a_from_Uin_Uquet
from blocks.measure_H import measure_H
from blocks.measure_Uout import measure_Uout
from helpers.signal_helper import convert_V_to_mV
from helpers.signal_helper import convert_mV_to_V
from helpers.signal_helper import setVpp
from helpers.csv_helper import read_in_transfer_function
from settings import project_path
from classes.signal_class import signal_class
from copy import copy
from blocks.determine_a import determine_a


import numpy as np


def evaluate_with_BBsignal(num_iters = 1) :


    f_rep = 900e3
    f_BB = 5e6
    Vpp = 0.3

    sample_rate_AWG_max = 2e8
    sample_rate_DSO = 9999e5

    Uout_ideal = generate_BBsignal(f_rep=f_rep, f_BB=f_BB, Vpp=Vpp, sample_rate_AWG_max=sample_rate_AWG_max, verbosity=0)

    H = measure_H(loadCSV=0, saveCSV=0, verbosity=1)
    a = determine_a(H, Uout_ideal, f_rep, Uout_ideal.sample_rate)

    K = compute_K_from_a(a=a, verbosity=0)

    Uquest_ideal = compute_Uquest_from_Uout(Uout=Uout_ideal, H=H, verbosity=0)

    Uin = compute_Uin_from_Uquest(Uquest=Uquest_ideal, K=K, verbosity=0)

    Uin_measured, Uout_measured = measure_Uout(Uin=Uin, sample_rate_AWG_max=sample_rate_AWG_max, loadCSV=0, saveCSV=0, id='2', verbosity=0)

    return Uout_ideal, Uout_measured
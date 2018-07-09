from blocks.generate_BBsignal import generate_BBsignal
from blocks.compute_Uquest_from_Uout import compute_Uquest_from_Uout
from blocks.compute_K_from_a import compute_K_from_a
from blocks.compute_Uin_from_Uquest import compute_Uin_from_Uquest
from blocks.compute_a_from_Uin_Uquet import compute_a_from_Uin_Uquet
from blocks.measure_H import measure_H
from blocks.measure_Uout import measure_Uout
from helpers.signalHelper import convert_V_to_mV
from helpers.signalHelper import convert_mV_to_V
from helpers.signalHelper import setVpp
from helpers.csvHelper import read_in_transfer_function
from global_data import project_path
from classes.signal_class import signal_class
from copy import copy

def determine_a(H, Uout_ideal, f_rep, sampleRateAWG):
    Uquest_ideal = compute_Uquest_from_Uout(Uout=Uout_ideal, H=H, verbosity=0)
    Uin = copy(Uquest_ideal)
    Uin.Vpp = 0.3
    Uin_measured, Uout_measured = measure_Uout(Uin=Uin, sample_rate_AWG_max=sampleRateAWG, loadCSV=0, saveCSV=0, id='1',
                                               verbosity=0)

    # save initial Data
    save_2cols(data_directory + 'Uin_0.csv', Uin_measured[:, 0], Uin_measured[:, 1])
    save_2cols(data_directory + 'Uout_0.csv', Uout_measured[:, 0], Uout_measured[:, 1])

    Uout_measured = Uout_measured.cut_one_period(f_rep)
    Uquest_measured = compute_Uquest_from_Uout(Uout=Uout_measured, H=H, verbosity=0)
    a = compute_a_from_Uin_Uquet(Uin=Uin, Uquest=Uquest_measured, N=3)
    return a
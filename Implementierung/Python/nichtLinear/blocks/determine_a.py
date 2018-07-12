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
from global_data import project_path
from classes.signal_class import signal_class
from copy import copy
from helpers.csv_helper import save_2cols

def determine_a(H, Uout_ideal, sample_rate_DSO, data_directory):
    Uquest_ideal = compute_Uquest_from_Uout(Uout=Uout_ideal, H=H, verbosity=0)
    Uin = copy(Uquest_ideal)
    Uin.Vpp = 0.6
    Uin_measured, Uout_measured = measure_Uout(Uin=Uin, sample_rate_DSO=sample_rate_DSO, loadCSV=0, saveCSV=0, id='1',
                                               verbosity=0)
    # save initial Data
    save_2cols(data_directory + 'Uin_0.csv', Uin_measured.time, Uin_measured.in_V)
    save_2cols(data_directory + 'Uout_0.csv', Uout_measured.time, Uout_measured.in_V)

    
#    f_rep_fix = 895.927e3        
#    Uout_measured = Uout_measured.cut_one_period(f_rep_fix)
    Uout_measured = Uout_measured.cut_one_period(Uin.f_rep)      
    
    Uquest_measured = compute_Uquest_from_Uout(Uout=Uout_measured, H=H, verbosity=0)
    a = compute_a_from_Uin_Uquet(Uin=Uin, Uquest=Uquest_measured, N=3)
    return a
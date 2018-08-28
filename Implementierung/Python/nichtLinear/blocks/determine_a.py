from blocks.compute_Uquest_from_Uout import compute_Uquest_from_Uout
from blocks.compute_a_from_Uin_Uquest import compute_a_from_Uin_Uquet
from blocks.measure_Uout import measure_Uout
from copy import copy
from helpers.csv_helper import save_2cols, save_signal
from helpers.overlay import overlay

def determine_a(H, Uout_ideal, sample_rate_DSO, data_directory):
    version = 1
    if version == 1:
        Uquest_ideal = compute_Uquest_from_Uout(Uout=Uout_ideal, H=H, verbosity=0)
        Uin = copy(Uquest_ideal)
        Uin.Vpp = 0.6
        Uin_measured, Uout_measured = measure_Uout(Uin=Uin, sample_rate_DSO=sample_rate_DSO, loadCSV=0, saveCSV=0, id='1',
                                                   verbosity=0)
    elif version == 2:
        # wird nicht verwendet
        # hier wird die Spannung am Ausgang als Referenzgenommen, diese wird so aber nicht erreicht
        Uout_ideal.Vpp = 6
        Uquest_ideal = compute_Uquest_from_Uout(Uout=Uout_ideal, H=H, verbosity=0)
        Uin = copy(Uquest_ideal)
        Uin_measured, Uout_measured = measure_Uout(Uin=Uin, sample_rate_DSO=sample_rate_DSO, loadCSV=0, saveCSV=0,
                                                   id='1',
                                                   verbosity=0)
    # save initial Data
    save_2cols(data_directory + 'Uin_initial.csv', Uin_measured.time, Uin_measured.in_V)
    save_2cols(data_directory + 'Uout_initial.csv', Uout_measured.time, Uout_measured.in_V)


    Uout_measured = Uout_measured.cut_one_period(Uin.f_rep)      
    
    Uquest_measured = compute_Uquest_from_Uout(Uout=Uout_measured, H=H, verbosity=0)
    save_signal(Uquest_measured, data_directory + 'Uquest_initial.csv')


    Uquest_measured = overlay(Uquest_measured, Uin)

    # plot_2_signals(Uin, Uquest_measured)

    a = compute_a_from_Uin_Uquet(Uin=Uin, Uquest=Uquest_measured, N=3)

    return a
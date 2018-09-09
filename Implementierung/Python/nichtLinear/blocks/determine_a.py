from blocks.compute_Uquest_from_Uout import compute_Uquest_from_Uout
from blocks.compute_a_from_Uin_Uquest import compute_a_from_Uin_Uquest
from blocks.measure_Uout import measure_Uout
from copy import copy
from helpers.csv_helper import save_2cols, save_signal
from helpers.overlay import overlay
from settings import polynomial_order, Vpp_for_determine_a, max_input_vpp_amplifier, save_signals_for_determine_a

def determine_a(H, Uout_ideal, sample_rate_DSO, data_directory):
    version = 1
    if version == 1:
        Uquest_ideal = compute_Uquest_from_Uout(Uout=Uout_ideal, H=H, verbosity=0)
        Uin = copy(Uquest_ideal)
        if Vpp_for_determine_a < 0.5*max_input_vpp_amplifier:
            print('Amplitude '+ str(Vpp_for_determine_a) +' V is probably too low for considerable nonlinearity!')
        
        Uin.Vpp = Vpp_for_determine_a
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
    


    Uout_measured = Uout_measured.cut_one_period(Uin.f_rep)      
    
    Uquest_measured = compute_Uquest_from_Uout(Uout=Uout_measured, H=H, verbosity=0)
    # save initial Data
    if save_signals_for_determine_a:
        save_2cols(data_directory + 'Uin_determine_a.csv', Uin_measured.time, Uin_measured.in_V)
        save_2cols(data_directory + 'Uout_determine_a.csv', Uout_measured.time, Uout_measured.in_V)
        save_signal(Uquest_measured, data_directory + 'Uquest_determine_a.csv')


    Uquest_measured = overlay(Uquest_measured, Uin)

    # plot_2_signals(Uin, Uquest_measured)

    a = compute_a_from_Uin_Uquest(Uin=Uin, Uquest=Uquest_measured, N=polynomial_order)

    return a
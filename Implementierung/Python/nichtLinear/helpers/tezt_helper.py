from helpers.csv_helper import load_ideal_signal, save_ideal_signal, save_ideal_a, load_ideal_a
from helpers.plot_helper import plot_2_signals, plot_2_transfer_functions, plot_2_Ks
from helpers.signal_helper import signals_are_equal, arrays_are_equal, transfer_functions_are_equal
import warnings
from classes.signal_class import signal_class
from classes.transfer_function_class import transfer_function_class
import numpy as np
from helpers.custom_value_error import custom_value_error


def finilize_tezt(values_computed, set_ideal_values, verbosity):

    if type(values_computed) is np.ndarray:

        if len(values_computed.shape) == 1:
            datatype = 'a'
        elif len(values_computed.shape) == 2:
            datatype = 'K'
        else:
            raise custom_value_error("The computed value is of an appropriate shape")

    elif isinstance(values_computed, signal_class):
        datatype = 'signal'
    elif isinstance(values_computed, transfer_function_class):
        datatype = 'transfer_function'
    else:
        raise custom_value_error("The computed value is of an appropriate shape")

    if datatype == 'signal':
        Uout_ideal_file_name = 'U_accepted.csv'
    elif datatype == 'transfer_function':
        Uout_ideal_file_name = 'H_accepted.csv'
    elif datatype == 'a' or datatype == 'K':
        Uout_ideal_file_name = datatype + '_accepted.csv'

    if set_ideal_values:
        values_ideal = values_computed
        save_ideal_signal(signal_ideal=values_ideal, filename=Uout_ideal_file_name, datatype=datatype)
        test_succeeded = True
        warnings.warn('This test will always succeed, since the ideal signal is being saved !')
    else:
        values_ideal = load_ideal_signal(filename=Uout_ideal_file_name, datatype=datatype)
        if datatype == 'signal':
            test_succeeded = signals_are_equal(values_computed, values_ideal)
        elif datatype == 'transfer_function':
            test_succeeded = transfer_functions_are_equal(values_computed, values_ideal)
        elif datatype == 'a' or datatype == 'K':
            test_succeeded = arrays_are_equal(values_computed, values_ideal)
    if verbosity:
        if datatype == 'signal':
            plot_2_signals(U1=values_ideal, U2=values_computed, legend1='U_ideal', legend2='U_computed')
        elif datatype == 'transfer_function':
            plot_2_transfer_functions(H1=values_ideal, H2=values_computed, legend1='H_ideal', legend2='H_computed')
        elif datatype == 'a':
            warnings.warn('a cannot be plotted')
        elif datatype == 'K':
            plot_2_Ks(K1=values_ideal, K2=values_computed, legend1='K_ideal', legend2='K_computed')


    return test_succeeded, values_ideal





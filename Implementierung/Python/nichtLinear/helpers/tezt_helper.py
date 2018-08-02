from helpers.csv_helper import load_ideal_signal, save_ideal_signal, save_ideal_a, load_ideal_a
from helpers.plot_helper import plot_2_signals
from helpers.signal_helper import signals_are_equal, arrays_are_equal
import warnings
from classes.signal_class import signal_class
import numpy as np


def finilize_tezt_with_signal(U_computed, set_ideal_signal, verbosity):

    if type(U_computed) is np.ndarray:

        if len(U_computed.shape) == 1:
            datatype = 'a'
        elif len(U_computed.shape) == 2:
            datatype = 'K'
        else:
            raise CustomValueError("The computed value is of an appropriate shape")

    elif isinstance(U_computed, signal_class):
        datatype = 'signal'

    else:
        raise CustomValueError("The computed value is of an appropriate shape")

    Uout_ideal_file_name = datatype + '_ideal'
    if set_ideal_signal:
        Uout_ideal = U_computed
        save_ideal_signal(signal_ideal=Uout_ideal, filename=Uout_ideal_file_name, datatype=datatype)
        test_succeeded = True
        warnings.warn('This test will always succeed, since the ideal signal is being saved !')
    else:
        Uout_ideal = load_ideal_signal(filename=Uout_ideal_file_name, datatype=datatype)
        if datatype == 'signal':
            test_succeeded = signals_are_equal(U_computed, Uout_ideal)
        elif datatype == 'a' or datatype == 'K':
            test_succeeded = arrays_are_equal(U_computed, Uout_ideal)
    if verbosity:
        if datatype == 'signal':
            plot_2_signals(U1=Uout_ideal, U2=U_computed, legend1='Uout_ideal', legend2='Uout_computed')
        elif datatype == 'a':
            warnings.warn('a cannot be plotted')
        elif datatype == 'K':
            plot_2_signals(U1=Uout_ideal, U2=U_computed, legend1='Uout_ideal', legend2='Uout_computed')


    return test_succeeded


class CustomValueError(ValueError):
 def __init__(self, arg):
  self.strerror = arg
  self.args = {arg}


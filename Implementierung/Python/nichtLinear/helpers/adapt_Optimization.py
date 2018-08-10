import numpy as np
from numpy import number

from classes.signal_class import signal_class

"""
In this file, some methods are implemented which are used to manipulate data used in the optimization methods of H and a.

created in August 2018
@Jonas Christ
"""


def zero_padding(signal, number):
    """
    This method adds zero-values to a signal to enlarge the period time.
    By this, the amount number is added at the beginning
        and number at the end making 2*number new values in total
    This is useful to reach a higher resolution in the frequency domain.
    This can just be used if the signal vanishs at the beginning / end of its period.
    An presumption taken is that the signal has an evenly spaced time axis.

    :param signal: the signal on which to add zero values. Instance of signal_class
    :param number:  the number of samples to be added at the beginning and end of signal each
    :return:
    """

    #TODO: Typechecking: is signal an instance of signal_class? are last values of signal really close to zero?
    delta_t = signal.timestep
    t_period = signal.length * delta_t
    time_to_append = np.linspace(t_period, t_period + 2*number * delta_t, 2*number, endpoint=False)
    zeros_to_append = np.zeros(number)

    new_time_axis = np.append(signal.time, time_to_append)
    new_values = np.append(np.append(zeros_to_append, signal.in_V), zeros_to_append)

    new_signal = signal_class(new_time_axis, new_values)

    return new_signal



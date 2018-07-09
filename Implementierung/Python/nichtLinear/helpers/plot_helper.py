import numpy as np
from scipy.interpolate import interp1d
import copy
from helpers.find_nearest import find_nearest
import matplotlib.pyplot as plt
from global_data import show_plots


def plot_two_signals(Uout_ideal, Uout_measured, legend1, legend2):
    plt.figure()
    plt.plot(Uout_measured.time, Uout_measured.in_V)
    plt.plot(Uout_ideal.time, Uout_ideal.in_V)
    plt.legend([legend1, legend2])
    plt.xlabel('t')
    plt.ylabel('U')
    if show_plots:
        plt.show()

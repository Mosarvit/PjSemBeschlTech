import numpy as np
from scipy.interpolate import interp1d
import copy
from helpers.find_nearest import find_nearest
import matplotlib.pyplot as plt
from global_data import show_plots


def plot_2_signals(U1, U2, legend1='U1', legend2='U2'):
    plt.figure()
    plt.plot(U2.time, U2.in_V)
    plt.plot(U1.time, U1.in_V)
    plt.legend([legend1, legend2])
    plt.xlabel('t')
    plt.ylabel('U')
    if show_plots:
        plt.show()

def plot_transfer_function(H, legend='H'):
    plt.figure()
    plt.plot(H.f, H.a)
    plt.legend([legend])
    plt.xlabel('f')
    plt.ylabel('Amplitude')
    if show_plots:
        plt.show()

    plt.figure()
    plt.plot(H.f, H.p)
    plt.legend([legend])
    plt.xlabel('f')
    plt.ylabel('phase')
    if show_plots:
        plt.show()

def plot_2_transfer_function_amplitudes(H1, H2,  legend1 = 'H1', legend2 = 'H2'):
    plt.figure()
    plt.plot(H1.f, H1.a, H2.f, H2.a)
    plt.legend([legend1, legend2])
    plt.xlabel('f')
    plt.ylabel('Amplitude')
    if show_plots:
        plt.show()
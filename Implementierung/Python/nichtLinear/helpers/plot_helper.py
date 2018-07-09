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

def plot_2_transfer_functions(H1, H2,  legend1 = 'H1', legend2 = 'H2'):
    f, axarr = plt.subplots(2, sharex=True)
    axarr[0].plot(H1.f, H1.a, H2.f, H2.a, )
    axarr[0].legend([legend1, legend2])

    axarr[1].plot(H1.f, H1.p, H2.f, H2.p)
    axarr[1].legend([legend1, legend2])

    if show_plots:
        plt.show()

def plot_transfer_function(H, legend1 = 'H'):

    f, axarr = plt.subplots(2, sharex=True)
    axarr[0].plot(H.f, H.a)
    axarr[0].legend([legend1])

    axarr[1].plot(H.f, H.p)
    axarr[1].legend([legend1])

    if show_plots:
        plt.show()
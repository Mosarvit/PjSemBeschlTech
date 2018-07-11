import numpy as np
from numpy import genfromtxt
import matplotlib as plt
from helpers.signal_evaluation import signal_evaluate

def test():
    """
    evaluates the given Uout with RF TOOL

    INPUT:

        Uout_filename - '_.csv'; Path to csv-file of the measured Uout
        results_filename - '_.csv'; Path to results.csv of all results

    OUTPUT:

        quality - skalar; result of the tool

    """
    Uout_filename = 'data/optimizer/adjust_H/Uout_2.csv'
    # wird nicht benötigt
    results_filename = 'data/optimizer/adjust_H/results.csv'

    quality = signal_evaluate(Uout_filename, results_filename)
    #print()
    return
test()

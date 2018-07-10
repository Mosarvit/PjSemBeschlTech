import numpy as np
from numpy import genfromtxt
import matplotlib as plt
from helpers.csv_helper import save_2cols
from tools.singlesine_Signal import Signal
from tools.singlesine_SineRef import SineRef
from tools.singlesine_Verzerrungszahlen import Verzerrungszahlen
from tools.singlesine_save_results import save



def test_evaluate():
    """
    evaluates the given Uout with RF TOOL

    INPUT:

        Uout_filename - '_.csv'; Path to csv-file of the measured Uout
        results_filename - '_.csv'; Path to results.csv of all results

    OUTPUT:

        quality - skalar; result of the tool

    """
    fBB = 5e6
    frev = 9e5
    csv = 1

    # Die Parameterübergabe ist noch nicht optimal

    for i in range(1,4):
        id = str(i)
        Uout_filename = 'csvDateien_K/Uout_' + id + '.csv'
        results_filename = 'csvDateien_K/results.csv'
        signal_output = Signal(dateiName=Uout_filename, frev=frev, fBB=fBB)

        dataPointsSignal, Vorzeichen, Startindex = signal_output[0:3]
        sineref_output = SineRef(frev=frev, fBB=fBB, dataPointsSignal=dataPointsSignal, Vorzeichen=Vorzeichen, Startindex=Startindex)

        flag = 'csvDateien_K/Uout_' + id + '.csv'
        dataPointsRef, PointsPulse, PulseOn, PulseA, PulseP = sineref_output[0:5]
        verzerrungszahlen_output = Verzerrungszahlen(dataPointsRef=dataPointsRef, dataPointsSignal=dataPointsSignal, PulseOn=PulseOn, PointsPulse=PointsPulse,
                                                     PulseA=PulseA, PulseP=PulseP, frev=frev, fBB=fBB, flag=flag)

        # quality aus verzerrungszahlen_output raus lesen!
        # print(verzerrungszahlen_output)
        # save(Ueberschreiben=0, input_file =verzerrungszahlen_output, output_file=results_filename)
    quality = 0
    return (quality)
test_evaluate()

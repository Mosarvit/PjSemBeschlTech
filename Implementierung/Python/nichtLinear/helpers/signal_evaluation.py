import numpy as np
from numpy import genfromtxt
import matplotlib as plt
from tools.singlesine_Signal import Signal
from tools.singlesine_SineRef import SineRef
from tools.singlesine_Verzerrungszahlen import Verzerrungszahlen
from tools.singlesine_save_results import save
import csv


def signal_evaluate(Uout_filename):
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

    # Die Parameterübergabe ist noch nicht optimal
    print(Uout_filename)
    signal_output = Signal(dateiName=Uout_filename, frev=frev, fBB=fBB)

    dataPointsSignal, Vorzeichen, Startindex = signal_output[0:3]
    sineref_output = SineRef(frev=frev, fBB=fBB, dataPointsSignal=dataPointsSignal, Vorzeichen=Vorzeichen,
                             Startindex=Startindex)

    flag = Uout_filename
    dataPointsRef, PointsPulse, PulseOn, PulseA, PulseP = sineref_output[0:5]
    verzerrungszahlen_output = Verzerrungszahlen(dataPointsRef=dataPointsRef, dataPointsSignal=dataPointsSignal,
                                                 PulseOn=PulseOn, PointsPulse=PointsPulse,
                                                 PulseA=PulseA, PulseP=PulseP, frev=frev, fBB=fBB, flag=flag)

    # quality aus verzerrungszahlen_output raus lesen!
    # print(verzerrungszahlen_output)
    with open(results_filename, 'w') as f:
        [f.write('{0},{1}\n'.format(key, value)) for key, value in verzerrungszahlen_output.items()]

    # save(Ueberschreiben=0, input_file =verzerrungszahlen_output, output_file=results_filename)
    quality = verzerrungszahlen_output['QGesamt1']
    print(quality)
    return (quality)

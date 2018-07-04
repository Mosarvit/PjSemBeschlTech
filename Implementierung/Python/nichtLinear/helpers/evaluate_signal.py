import numpy as np
from numpy import genfromtxt
import matplotlib as plt
from helpers.csvHelper import save_2cols
from tools.singlesine_Signal import Signal
from tools.singlesine_SineRef import SineRef
from tools.singlesine_Verzerrungszahlen import Verzerrungszahlen
from tools.singlesine_save_results import save

# dateiName='csvDateien_K/Messung_060_TD_y_1.csv'
# signal_output='Signal_output.csv'
# fBB='5e6'
# frev='9e5'
# csv='1'
# #Testing singlesine_Signal
# python singlesine_Signal.py -i $dateiName -o $signal_output -frev $frev -fBB $fBB --debug
#
# #Testing singlesine_SineRef
# sineref_output='SineRef_output.csv'
# python singlesine_SineRef.py -i $signal_output -o $sineref_output -frev $frev -fBB $fBB -csv $csv --debug
#
# #Testing singlesine_Verzerrungszahlen
# verzerrungszahlen_output='verzerrungszahlen_output.csv'
# python singlesine_Verzerrungszahlen.py -i $dateiName -signal $signal_output -ref $sineref_output -o $verzerrungszahlen_output -frev $frev -fBB $fBB -csv $csv --debug
#
#
# # Testing singlesine_save_results
# python singlesine_save_results.py -i $verzerrungszahlen_output -u '0' -o 'results.csv'



def evaluate_signal(Uout_filename, results_filename):
    """
    evaluates the given Uout with RF TOOL

    INPUT:

        Uout_filename - '_.csv'; Path to csv-file of the measured Uout
        results_filename - '_.csv'; Path to results.csv of all results

    OUTPUT:

        quality - skalar; results of the tool

    """
    fBB='5e6'
    frev='9e5'
    csv = '1'
    signal_output = Signal(dateiName=Uout_filename, frev=frev, fBB=fBB)

    sineref_output = SineRef(frev=frev, fBB=fBB, signal_output=signal_output, csv=csv)

    verzerrungszahlen_output = Verzerrungszahlen(dataPointsRef=sineref_output, dataPointsSignal=signal_output)
    # quality aus verzerrungszahlen_output raus lesen!!!
    print(verzerrungszahlen_output)
    save(Ueberschreiben='0', verzerrungszahlen_output=verzerrungszahlen_output, output_file=results_filename)
    quality = 0
    return (quality)
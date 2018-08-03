import numpy as np
from helpers.signal_evaluation import signal_evaluate
from settings import *

def function():
    data_directory = project_path + 'data/optimizer/adjust_H_19_07_2018-10_58_39/'
    quality = signal_evaluate(data_directory + 'Uout_measured_' + id + '.csv',
                              data_directory + 'quality_' + id + '.csv')

    return

function()
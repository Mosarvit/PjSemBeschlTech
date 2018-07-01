# Mit dieser Routine kann evaluiert werden, ob adjust_H zur Verbessrung des Uout führt.
# Um unabhängig von K zu sein, sollte diese im niedrigen Amplitudenbereich arbeiten.
# Eine Idee wäre, adjust_H in einer Schleife mehrmals auszuführen und den Fehler zu speichern und dann zu plotten.

from blocks.generate_BBsignal import generate_BBsignal
from blocks.compute_Uquest_from_Uout import compute_Uquest_from_Uout
from blocks.compute_K_from_a import compute_K_from_a
from blocks.compute_Uin_from_Uquest import compute_Uin_from_Uquest
from blocks.compute_a_from_Uin_Uquet import compute_a_from_Uin_Uquet
from blocks.measure_H import measure_H
from blocks.adjust_H import adjust_H
from blocks.adjust_a import adjust_a
from blocks.measure_Uout import measure_Uout
from helpers.signalHelper import convert_V_to_mV
from helpers.signalHelper import convert_mV_to_V
from helpers.signalHelper import setVpp
from helpers.signalHelper import cun_one_period
from helpers.csvHelper import save_2cols
from helpers.csvHelper import read_in_transfer_function
from adts.transfer_function import transfer_function

import csv
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
from scipy import linalg


def evaluate():
    # Initialization
    sampleRateAWG = 999900000
    f_rep = 900e3
    f_BB = 5e6
    Vpp = 0.3

    Uout_ideal = generate_BBsignal(f_rep=f_rep, f_BB=f_BB, Vpp=Vpp, sampleRateAWG=sampleRateAWG, verbosity=0)

    H = measure_H(loadCSV=True, saveCSV=False, verbosity=0)
    Uquest_ideal = compute_Uquest_from_Uout(Uout=np.transpose(Uout_ideal), H=H, verbosity=0)

    Uin = setVpp(Uquest_ideal, Vpp)

    for i in range(0,11):
        id = str(i)
        # Uin_measured, Uout_measured = measure_Uout(Uin=Uin, sampleRateAWG=sampleRateAWG, loadCSV=True, saveCSV=False, id=i, verbosity=1)
        Uout_measured = genfromtxt('data/current_data/Uout_2.csv', delimiter=',')
        Uin_measured = genfromtxt('data/current_data/Uout_2.csv', delimiter=',')
        save_2cols('data/optimizer/Uin_' + id + '.csv', Uin_measured[:, 0], Uin_measured[:, 1])
        save_2cols('data/optimizer/Uout_' + id + '.csv', Uout_measured[:, 0], Uout_measured[:, 1])

        # begin cut just one period out of Uout_measured
        Uout_measured = cun_one_period(Uout_measured, f_rep)

        # compute new Uin
        Uquest_measured = compute_Uquest_from_Uout(Uout=Uout_measured, H=H, verbosity=0)
        Uquest_measured_mV = convert_V_to_mV(Uquest_measured)

        Uin_mV = convert_V_to_mV(Uin)

        a = compute_a_from_Uin_Uquet(Uin=Uin_mV, Uquest=Uquest_measured_mV, N=3)
        K = compute_K_from_a(a=a, verbosity=0)
        with open('data/optimizer/a_' + id + '.csv', 'w+', newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for k in range(0, len(a)):
                writer.writerow([a[k]])
        save_2cols('data/optimizer/K_' + id + '.csv', K[:, 0], K[:, 1])
        save_2cols('data/optimizer/K_' + id + '.csv', K[:,0], K[:,1])

        Uquest_ideal_mV = convert_V_to_mV(Uquest_ideal)
        Uin_mV = compute_Uin_from_Uquest(Uquest=Uquest_ideal_mV, K=K, verbosity=0)
        Uin = convert_mV_to_V(Uin_mV)

        # adjust H
        sigma_H = 1
        # H = adjust_H(H, Uout_measured, Uout_ideal,sigma_H=sigma_H)
        save_2cols('data/optimizer/H_a_' + id + '.csv', H.f, H.a)
        save_2cols('data/optimizer/H_p_' + id + '.csv', H.f, H.p)

    return
evaluate()
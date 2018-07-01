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
from blocks.measure_Uout import measure_Uout
from helpers.signalHelper import convert_V_to_mV
from helpers.signalHelper import convert_mV_to_V
from helpers.signalHelper import setVpp
from helpers.signalHelper import cun_one_period
from helpers.csvHelper import save_2cols
from helpers.csvHelper import read_in_transfer_function
from adts.transfer_function import transfer_function

import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
from scipy import linalg


def evaluate():

    sampleRateAWG = 999900000
    f_rep = 900e3
    f_BB = 5e6
    Vpp = 0.3

    Uout_ideal = generate_BBsignal(f_rep=f_rep, f_BB=f_BB, Vpp=Vpp, sampleRateAWG=sampleRateAWG, verbosity=0)

    H = measure_H(loadCSV=True, saveCSV=False, verbosity=0)
    Uquest_ideal = compute_Uquest_from_Uout(Uout=np.transpose(Uout_ideal), H=H, verbosity=0)

    Uin = setVpp(Uquest_ideal, Vpp)

    # Uin_measured, Uout_measured = measure_Uout(Uin=Uin, sampleRateAWG=sampleRateAWG, loadCSV=True, saveCSV=True, id='1', verbosity=0)
    Uout_measured = genfromtxt('data/current_data/Uout_1.csv', delimiter=',')
    Uin_measured = genfromtxt('data/current_data/Uout_1.csv', delimiter=',')

    # begin cut just one period out of Uout_measured
    Uout_measured = cun_one_period(Uout_measured, f_rep)


    Uquest_measured = compute_Uquest_from_Uout(Uout=Uout_measured, H=H, verbosity=0)
    Uquest_measured_mV = convert_V_to_mV(Uquest_measured)

    Uin_mV = convert_V_to_mV(Uin)

    a = compute_a_from_Uin_Uquet(Uin=Uin_mV, Uquest=Uquest_measured_mV, N=3)
    K = compute_K_from_a(a=a, verbosity=0)

    Uquest_ideal_mV = convert_V_to_mV(Uquest_ideal)

    Uin_mV = compute_Uin_from_Uquest(Uquest=Uquest_ideal_mV, K=K, verbosity=0)

    Uin = convert_mV_to_V(Uin_mV)

    # Uin_measured, Uout_measured = measure_Uout(Uin=Uin, sampleRateAWG=sampleRateAWG, loadCSV=False, saveCSV=True, id='2', verbosity=1)
    Uout_measured = genfromtxt('data/current_data/Uout_2.csv', delimiter=',')
    Uin_measured = genfromtxt('data/current_data/Uout_2.csv', delimiter=',')

    save_2cols('tools/csvDateien_K/Uout_2.csv', Uout_measured[:,0], Uout_measured[:,1])

    #H anpassen
    sigma_H = 1
    H_neu = H#= adjust_H(H, Uout_ideal=Uout_ideal, Uout_measured=Uout_measured, sigma_H=sigma_H)

    U_quest2 = compute_Uquest_from_Uout(Uout=np.transpose(Uout_ideal), H=H_neu, verbosity=0)
    U_quest2 = setVpp(U_quest2, Vpp)
    U_quest2 = convert_V_to_mV(U_quest2)

    Uin_mV = compute_Uin_from_Uquest(Uquest=U_quest2, K=K, verbosity=0)
    Uin = convert_mV_to_V(Uin_mV)

    # Uin_measured, Uout_measured = measure_Uout(Uin=Uin, sampleRateAWG=sampleRateAWG, loadCSV=False, saveCSV=True, id='3', verbosity=1)
    Uout_measured = genfromtxt('data/current_data/Uout_3.csv', delimiter=',')
    Uin_measured = genfromtxt('data/current_data/Uout_3.csv', delimiter=',')

    save_2cols('tools/csvDateien_K/Uout_3.csv', Uout_measured[:, 0], Uout_measured[:, 1])



    return
evaluate()
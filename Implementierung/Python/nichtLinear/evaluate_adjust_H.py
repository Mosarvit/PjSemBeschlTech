# Mit dieser Routine kann evaluiert werden, ob adjust_H zur Verbessrung des Uout führt.
# Um unabhängig von K zu sein, sollte diese im niedrigen Amplitudenbereich arbeiten.
# Eine Idee wäre, adjust_H in einer Schleife mehrmals auszuführen und den Fehler zu speichern und dann zu plotten.

from blocks.generate_BBsignal import generate_BBsignal
from blocks.compute_Uquest_from_Uout import compute_Uquest_from_Uout
from blocks.compute_K_from_a import compute_K_from_a
from blocks.compute_Uin_from_Uquest import compute_Uin_from_Uquest
from blocks.compute_a_from_Uin_Uquet import compute_a_from_Uin_Uquet
# from helpers.evaluate_signal import evaluate_signal
from blocks.measure_H import measure_H
from blocks.adjust_H import adjust_H
from blocks.adjust_a import adjust_a
from blocks.measure_Uout import measure_Uout
from helpers.signalHelper import convert_V_to_mV
from helpers.signalHelper import convert_mV_to_V
from helpers.signalHelper import setVpp
from helpers.signalHelper import cun_one_period
from helpers.csvHelper import save_2cols
# from tools.test_evaluation import test_evaluate
from helpers.csvHelper import read_in_transfer_function
from adts.transfer_function import transfer_function

import csv
import numpy as np
from numpy import genfromtxt
import matplotlib.pyplot as plt
from scipy import linalg
from global_data import project_path


def evaluate():
    # Initialization
    sampleRateDSO = 999900000
    f_rep = 900e3
    sampleRateAWG = 223*f_rep    
    f_BB = 5e6
    Vpp = 0.3

    Uout_ideal = generate_BBsignal(f_rep=f_rep, f_BB=f_BB, Vpp=Vpp, sampleRateAWG=sampleRateAWG, verbosity=1)


    H = measure_H(loadCSV=1, saveCSV=True, verbosity=0)
    # save initial H
    save_2cols('tools/adjustH/Ha_0.csv', H.f, H.a)
    save_2cols('tools/adjustH/Hp_0.csv', H.f, H.p)

    Uquest_ideal = compute_Uquest_from_Uout(Uout=np.transpose(Uout_ideal), H=H, verbosity=1)

    Uin = setVpp(Uquest_ideal, Vpp)
    
    Uin_measured, Uout_measured = measure_Uout(Uin=Uin, sampleRateAWG=sampleRateAWG, sampleRateDSO=sampleRateDSO, loadCSV=0, saveCSV=True, id='1', verbosity=0)
    return
    # Uin_measured = genfromtxt('data/current_data/Uin_2.csv', delimiter=',')
    # Uout_measured = genfromtxt('data/current_data/Uout_2.csv', delimiter=',')
    # begin cut just one period out of Uout_measured
    Uout_measured = cun_one_period(Uout_measured, f_rep)
    Uin_measured = cun_one_period(Uout_measured, f_rep)
    #return

    # save initial Data
    save_2cols('tools/adjustH/Uin_0.csv', Uin_measured[:, 0], Uin_measured[:, 1])
    save_2cols('tools/adjustH/Uout_0.csv', Uout_measured[:, 0], Uout_measured[:, 1])

    Uquest_measured = compute_Uquest_from_Uout(Uout=Uout_measured, H=H, verbosity=0)
    Uquest_measured_mV = convert_V_to_mV(Uquest_measured)

    Uin_mV = convert_V_to_mV(Uin)

    a = compute_a_from_Uin_Uquet(Uin=Uin_mV, Uquest=Uquest_measured_mV, N=3)
    K = compute_K_from_a(a=a, verbosity=0)

    # save K
    save_2cols('tools/adjustH/K_0.csv', K[:, 0], K[:, 1])

    for i in range(1,2):
        id = str(i)
        # compute new Uin
        Uquest_ideal = compute_Uquest_from_Uout(Uout=np.transpose(Uout_ideal), H=H, verbosity=0)
        Uquest_ideal_mV = convert_V_to_mV(Uquest_ideal)

        Uin_mV = compute_Uin_from_Uquest(Uquest=Uquest_ideal_mV, K=K, verbosity=0)

        Uin = convert_mV_to_V(Uin_mV)

        Uin_measured, Uout_measured = measure_Uout(Uin=Uin, sampleRateAWG=sampleRateAWG, sampleRateDSO=sampleRateDSO, loadCSV=False, saveCSV=False, id=id, verbosity=1)
        # Uin_measured = genfromtxt('data/current_data/Uin_2.csv', delimiter=',')
        # Uout_measured = genfromtxt('data/current_data/Uout_2.csv', delimiter=',')
        smlrt = 1 / ( Uout_measured[11,0] - Uout_measured[10,0] )
        # begin cut just one period out of Uout_measured
        Uout_measured = cun_one_period(Uout_measured, f_rep)
        Uin_measured = cun_one_period(Uin_measured, f_rep)
        return
        # save Uin and Uout
        save_2cols('tools/adjustH/Uin_' + id + '.csv', Uin_measured[:, 0], Uin_measured[:, 1])
        save_2cols('tools/adjustH/Uout_' + id + '.csv', Uout_measured[:, 0], Uout_measured[:, 1])
        save_2cols('tools/csvDateien_K/Uout_' + id + '.csv', Uout_measured[:, 0], Uout_measured[:, 1])

        # quality = evaluate_signal('tools/csvDateien_K/Uout_' + id + '.csv', 'csvDateien_K/results_adjust_H.csv')
        sigma_H = 0.5
#        sampleRateAWG = Uout_measured.shape[0]
#        print(sampleRateAWG)
#        Uout_ideal_compute = generate_BBsignal(f_rep=f_rep, f_BB=f_BB, Vpp=Vpp, sampleRateAWG=sampleRateAWG, verbosity=0)
        H = adjust_H(H, np.transpose(Uout_ideal), Uout_measured, sigma_H=sigma_H, verbosity=True) # transponiertes Uout_ideal???
        save_2cols('tools/adjustH/Ha_' + id + '.csv', H.f, H.a)
        save_2cols('tools/adjustH/Hp_' + id + '.csv', H.f, H.p)
        
        Ha_0 = genfromtxt('tools/adjustH/Ha_0.csv', delimiter=',')
        # Ha_1 = genfromtxt('tools/adjustH/H_a_1.csv', delimiter=',')
        fig = plt.figure(1)
        plt.plot(Ha_0[:,0], Ha_0[:,1],'r',H.f, H.a, 'b')
        plt.title('Runde 0 - rot, Runde ' + id + ' - blau')
        plt.xlabel('f')
        plt.ylabel('Ha')
        plt.show()
    # quality = test_evaluate()

    verbosity = False
    if verbosity:
        Ha_0 = genfromtxt('tools/adjustH/Ha_0.csv', delimiter=',')
        Ha_1 = genfromtxt('tools/adjustH/Ha_1.csv', delimiter=',')
        fig = plt.figure(1)
        plt.plot(Ha_0[:,0], Ha_0[:,1],'r',Ha_1[:,0], Ha_1[:,1], 'b')
        plt.title('Runde 1 - rot, Runde 3 - blau')
        plt.xlabel('f')
        plt.ylabel('Ha')
        plt.show()
        
        Uout_measured1 = genfromtxt('tools/csvDateien_K/Uout_1.csv', delimiter=',')
        Uout_measured10 = genfromtxt('tools/csvDateien_K/Uout_3.csv', delimiter=',')
        fig = plt.figure(1)
        plt.plot(Uout_measured1[:,0], Uout_measured1[:,1],'r',Uout_measured10[:,0], Uout_measured10[:,1], 'b')
        plt.title('Runde 1 - rot, Runde 3 - blau')
        plt.xlabel('t')
        plt.ylabel('U')
        plt.show()

    return
evaluate()
from compute import generate_BBsignal
from compute import compute_Uquest_from_Uout
from measure import measure_Uout, measure_H
from compute import compute_a_from_Uin_Uquet, compute_K_from_a, compute_Uin_from_Uquest
import numpy as np
from helpers import conform_to_sampleRateAWG, find_nearest
import matplotlib.pyplot as plt


def evaluate() :

    verbosity = 0
    sampleRateAWG = 999900000
    f_rep = 900e3
    f_BB = 5e6

    Uout_ideal = generate_BBsignal.generate(f_rep=f_rep, f_BB=f_BB, vpp=.3, verbosity=1)


    H = measure_H.measure(loadCSV=True, saveCSV=True, verbosity=verbosity)
    Uquest_ideal = compute_Uquest_from_Uout.compute(Uout=np.transpose(Uout_ideal), H=H, verbosity=verbosity)
    Uin = conform_to_sampleRateAWG.conform(Uin=Uquest_ideal, sampleRateAWG=sampleRateAWG)
    Uout_measured = measure_Uout.measure(Uin=Uin, Vpp=0.3, loadCSV=True, saveCSV=True, id='1', verbosity=verbosity)

    T=1/f_rep
    indT = find_nearest.find1(Uout_measured[:, 0], T + Uout_measured[0, 0])
    Uout_measured = Uout_measured[0:indT, :]

    plt.figure()
    plt.plot(Uout_measured)
    plt.title('Uout_measured')
    plt.ylabel('u')
    plt.ylabel('t')
    plt.show()

    Uquest_measured=compute_Uquest_from_Uout.compute(Uout=Uout_measured, H=H, verbosity=verbosity)
    a = compute_a_from_Uin_Uquet.compute(Uin=Uin, Uquest=Uquest_measured, N=3, verbosity=verbosity)
    K = compute_K_from_a.compute(a=a, verbosity=True)
    Uin = compute_Uin_from_Uquest.compute(Uquest=Uquest_ideal, K=K, sampleRateAWG=sampleRateAWG, verbosity=verbosity)

    Uout_measured = measure_Uout.measure(Uin=Uin, loadCSV=False, saveCSV=True, id='2', verbosity=verbosity)





evaluate()
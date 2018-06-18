from blocks import generate_BBsignal, compute_Uquest_from_Uout, compute_K_from_a, compute_Uin_from_Uquest, \
    compute_a_from_Uin_Uquet, measure_Uout, measure_H
import numpy as np
from helpers import find_nearest
import matplotlib.pyplot as plt
from helpers import signalHelper, globalVars
from scipy import linalg


def evaluate() :


    sampleRateAWG = 999900000
    f_rep = 900e3
    f_BB = 5e6
    Vpp = 0.3

    Uout_ideal = generate_BBsignal.generate(f_rep=f_rep, f_BB=f_BB, Vpp=Vpp, sampleRateAWG=sampleRateAWG, verbosity=0)


    H = measure_H.measure(loadCSV=True, saveCSV=True, verbosity=0)
    Uquest_ideal = compute_Uquest_from_Uout.compute(Uout=np.transpose(Uout_ideal), H=H, verbosity=0)

    Uin = signalHelper.setVpp(Uquest_ideal, Vpp)

    # csvHelper.save_2cols('data/test_data/Uin_our.csv', Uin[:,0], Uin[:,1])

    Uout_measured = measure_Uout.measure(Uin=Uin, sampleRateAWG=sampleRateAWG, loadCSV=True, saveCSV=True, id='1', verbosity=0)

    # begin cut just one period out of Uout_measured

    T=1/f_rep
    indT = find_nearest.find1(Uout_measured[:, 0], T + Uout_measured[0, 0])
    Uout_measured = Uout_measured[0:indT, :]

    # end
    # begin plot cut Uout

    # fig = plt.figure()
    # plt.plot(Uout_measured[:,0], Uout_measured[:,1])
    # plt.title('Uout_measured')
    # plt.xlabel('t')
    # plt.ylabel('U')
    # if globalVars.showPlots :
    #     plt.show()
    # fig.savefig('../../../ErstellteDokumente/Zwischenpraesentation/slides/ResultCode/plots/Uout_measured_cut.pdf')

    # end

    Uquest_measured = compute_Uquest_from_Uout.compute(Uout=Uout_measured, H=H, verbosity=0)
    Uquest_measured_mV = signalHelper.convert_V_to_mV(Uquest_measured)


    Uin_mV = signalHelper.convert_V_to_mV(Uin)

    a = compute_a_from_Uin_Uquet.compute(Uin=Uin_mV, Uquest=Uquest_measured_mV, N=3, verbosity=0)
    K = compute_K_from_a.compute(a=a, verbosity=0)

    Uquest_ideal_mV = signalHelper.convert_V_to_mV(Uquest_ideal)

    Uin_mV = compute_Uin_from_Uquest.compute(Uquest=Uquest_ideal_mV, K=K, verbosity=1)

    Uin = signalHelper.convert_mV_to_V(Uin_mV)

    Uout_measured = measure_Uout.measure(Uin=Uin, sampleRateAWG=sampleRateAWG, loadCSV=False, saveCSV=True, id='2', verbosity=0)





evaluate()
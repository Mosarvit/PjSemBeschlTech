from compute import generate_BBsignal
from compute import compute_Uquest_from_Uout
from measure import measure_Uout, measure_H
from compute import compute_a_from_Uin_Uquet, compute_K_from_a, compute_Uin_from_Uquest
import numpy as np
from helpers import conform_to_sampleRateAWG


def evaluate() :

    verbosity = 1
    sampleRateAWG = 999900000

    Uout_ideal = generate_BBsignal.generate(vpp=.3, verbosity=verbosity)

    H = measure_H.measure(loadCSV=True, saveCSV=True, verbosity=verbosity)
    Uquest_ideal = compute_Uquest_from_Uout.compute(Uout=np.transpose(Uout_ideal), H=H, verbosity=verbosity)
    Uin = conform_to_sampleRateAWG.conform(Uin=Uquest_ideal, sampleRateAWG=sampleRateAWG)
    Uout_measured = measure_Uout.measure(Uin=Uin, loadCSV=True, saveCSV=True, id='1', verbosity=verbosity)
    Uquest_measured=compute_Uquest_from_Uout.compute(Uout=Uout_measured, H=H, verbosity=verbosity)
    a = compute_a_from_Uin_Uquet.compute(Uin=Uin, Uquest=Uquest_measured, N=3, verbosity=verbosity)
    K = compute_K_from_a.compute(a=a, verbosity=verbosity)
    Uin = compute_Uin_from_Uquest.compute(Uquest=Uquest_ideal, K=K, sampleRateAWG=sampleRateAWG, verbosity=verbosity)

    Uout_measured = measure_Uout.measure(Uin=Uin, loadCSV=False, saveCSV=True, id='2', verbosity=verbosity)





evaluate()
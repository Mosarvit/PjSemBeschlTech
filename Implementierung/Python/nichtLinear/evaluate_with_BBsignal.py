from compute import generate_BBsignal
from compute import compute_Uquest_from_Uout
from measure import measure_Uout, measure_H
from compute import compute_a_from_Uin_Uquet, compute_K_from_a, compute_Uin_from_Uquest


def evaluate() :

    verbosity = 1
    loadCSV = 1

    Uout_ideal = generate_BBsignal.generate(verbosity=verbosity)

    H = measure_H.measure(loadCSV=loadCSV, saveCSV=True, verbosity=verbosity)
    Uquest_ideal = compute_Uquest_from_Uout.compute(Uout=Uout_ideal, H=H, verbosity=verbosity)
    Uin = Uquest_ideal

    Uout_measured = measure_Uout.measure(Uin=Uin, loadCSV=False, saveCSV=True, id='1', verbosity=verbosity)
    Uquest_measured=compute_Uquest_from_Uout.compute(Uout=Uout_measured, H=H, verbosity=verbosity)
    a = compute_a_from_Uin_Uquet.compute(Uin=Uin, Uquest=Uquest_measured, N=3, verbosity=verbosity)
    K = compute_K_from_a.compute(a=a, verbosity=verbosity)
    Uin = compute_Uin_from_Uquest.compute(Uquest=Uquest_ideal, K=K, verbosity=verbosity)

    Uout_measured = measure_Uout.measure(Uin=Uin, loadCSV=False, saveCSV=True, id='2', verbosity=verbosity)

evaluate()
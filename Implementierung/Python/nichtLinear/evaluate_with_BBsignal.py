from compute import generate_BBsignal
from compute import compute_Uquest_from_Uout
from measure import measure_Uout, measure_H
from compute import compute_a_from_Uin_Uquet, compute_K_from_a, compute_Uin_from_Uquest


def evaluate() :

    verbosity = 1
    loadCSV = 1

    Uout_ideal = generate_BBsignal.generate(verbosity=verbosity)
    H = measure_H.measure(loadCSV, verbosity)
    Uquest_ideal = compute_Uquest_from_Uout.compute(Uout_ideal, H, verbosity)
    Uin = Uquest_ideal
    Uout_measured = measure_Uout.measure(Uin, verbosity)
    Uquest_measured=compute_Uquest_from_Uout.compute(Uout_measured, H, verbosity)
    N=3 # degree of a
    a = compute_a_from_Uin_Uquet.compute(Uin, Uquest_measured, N, verbosity)
    K = compute_K_from_a.compute(a, verbosity)
    Uin = compute_Uin_from_Uquest.compute(Uquest_ideal, K, verbosity)
    Uout_measured = measure_Uout(Uin, verbosity)


evaluate()
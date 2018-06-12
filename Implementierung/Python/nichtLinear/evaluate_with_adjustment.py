from compute import generate_BBsignal
from compute import compute_Uquest_from_Uout
from measure import measure_Uout, measure_H
from compute import compute_a_from_Uin_Uquet, compute_K_from_a, compute_Uin_from_Uquest
from adjust import adjust_H, adjust_a

def evaluate() :

    verbosity = 1
    loadCSV = 1

    Uout_ideal = generate_BBsignal.generate(verbosity=verbosity)
    H = measure_H.measure(loadCSV, verbosity)
    Uquest_ideal = compute_Uquest_from_Uout.compute(Uout_ideal, H, verbosity)
    Uin = Uquest_ideal
    Uout_measured = measure_Uout(Uin, verbosity)
    Uquest_measured=compute_Uquest_from_Uout(Uout_measured, H, verbosity)
    N=3 # degree of a
    a = compute_a_from_Uin_Uquet.compute(Uin, Uquest_measured, N, verbosity)
    K = compute_K_from_a.compute(a, verbosity)
    Uin = compute_Uin_from_Uquest.compute(Uquest_ideal, K, verbosity)
    Uout_measured = measure_Uout(Uin, verbosity)

    # adjustment

    sigma_H = 0.5
    sigma_quest = 0.5
    Hneu = adjust_H(H, Uout_ideal, Uout_measured, sigma_H )
    aneu = adjust_a(a, Uin, Uout_measured, sigma_quest )
    Kneu = compute_K_from_a.compute(aneu, verbosity)

    Uquest_ideal_adj = compute_Uquest_from_Uout.compute(Uout_ideal, Hneu, verbosity)
    Uin_adj = compute_Uin_from_Uquest.compute(Uquest_ideal_adj, Kneu, verbosity)
    Uout_measured_adj = measure_Uout(Uin_adj, verbosity)

evaluate()
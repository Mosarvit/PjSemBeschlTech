
import measure_H

from compute import create_BBsignal
from compute import compute_Uquest_from_Uout
import measure_Uout
from compute import compute_a_from_Uin_Uquet, compute_K_from_a, compute_Uin_from_Uquest

def evaluateWithSomeU_out() :

    verbosity = 1

    Uout_ideal = create_BBsignal.create(fq1=50, fq2=20, vpp=300)
    H = measure_H.measure()
    Uquest_ideal = compute_Uquest_from_Uout.compute(Uout_ideal, H, verbosity)
    Uin = Uquest_ideal
    Uout_measured = measure_Uout(Uin, verbosity)
    Uquest_measured=compute_Uquest_from_Uout(Uout_measured, H, verbosity)
    N=3 # degree of a
    a = compute_a_from_Uin_Uquet.compute(Uin, Uquest_measured, N, verbosity)
    K = compute_K_from_a.compute(a, verbosity)
    Uin = compute_Uin_from_Uquest.compute(Uquest_ideal, K, verbosity)
    Uout_measured = measure_Uout(Uin)




import measure_H

from compute import create_BBsignal
from compute import compute_Uquest_from_Uout

def evaluateWithSomeU_out() :
    fq1 = 50
    fq2 = 20
    vpp = 300
    Uout_ideal = create_BBsignal.create(fq1, fq2, vpp)
    H = measure_H.measure()
    Uquest_ideal = compute_Uquest_from_Uout.compute()



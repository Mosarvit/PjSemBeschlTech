from scipy import linalg
from later import getBB_Uout

f_rep = 10e2
f_bb = 10e3
f_g = 40e3
Samplingrate = 999900000

Uout_ideal = computeIdealBBsignal(f_rep, f_bb, f_g, Samplingrate)
Uout_real = getBB_Uout.get(f_rep, f_bb, f_g, Samplingrate)

err = linalg.norm(Uout_real - Uout_ideal) / linalg.norm(Uout_ideal)
print(err)
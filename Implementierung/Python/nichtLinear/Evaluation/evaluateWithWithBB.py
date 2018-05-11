from scipy import linalg
from later import getBB_Uout

f_rep = 10e2
f_bb = 10e3
f_g = 40e3
Samplingrate = 999900000

U_out_ideal = computeIdealBBsignal(f_rep, f_bb, f_g, Samplingrate)
U_out_real = getBB_Uout.get(f_rep, f_bb, f_g, Samplingrate)

err = linalg.norm(U_out_real - U_out_ideal) / linalg.norm(U_out_ideal)
print(err)
from scipy import linalg
import getBB_U_out

f_rep = 10e2
f_bb = 10e3
f_g = 40e3
Samplingrate = 999900000

U_out_ideal = computeIdealBBsignal(f_rep, f_bb, f_g, Samplingrate)
U_out_real = getBB_U_out.get(f_rep, f_bb, f_g, Samplingrate)

err = linalg.norm(U_out_real - U_out_ideal) / linalg.norm(U_out_ideal)
print(err)
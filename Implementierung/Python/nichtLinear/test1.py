from numpy import genfromtxt
import Param_Signal as param
import numpy as np

u_quest_300_matlab = genfromtxt('testdata/u_quest_300.csv', delimiter=',')
U_in = np.transpose(genfromtxt('testdata/U_in.csv', delimiter=',')[:,1])

vpp=300e-3
N=3

[ a, K ] = param.computeParam(U_in,vpp,u_quest_300_matlab,N)

# err = linalg.norm(u_quest - u_quest_300_matlab) / linalg.norm(u_quest_300_matlab)
# print(err)
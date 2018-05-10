# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 11:22:44 2017

@author: denys
"""
def get(f_rep, f_bb, f_g, N, toPlot):

    import getH
    import computea
    import numpy as np
    from Helpers import writeAWG, writeDSO
    import computeU_quest_fromBBsignal

    a = read_a_FromCSV()
    [frq, H, PhaseH] = read_H_FromCSV()

    samplerateAWG = 999900000

    U_quest = computeU_quest_fromBBsignal.compute(f_rep, f_bb, f_g, samplerateAWG, frq, H, PhaseH)
    U_in = computeU_in.compute(U_quest, a)

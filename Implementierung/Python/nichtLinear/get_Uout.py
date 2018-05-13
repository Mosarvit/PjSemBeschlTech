# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 11:22:44 2017

@author: denys
"""
from compute import compute_Uin_from_Uquest


def get(f_rep, f_bb, f_g, N, toPlot):

    from later import compute_Uquest_from_BBUout

    a = read_a_FromCSV()
    [frq, H, PhaseH] = read_H_FromCSV()

    samplerateAWG = 999900000

    Uquest = compute_Uquest_from_BBUout.compute(f_rep, f_bb, f_g, samplerateAWG, frq, H, PhaseH)
    Uin = compute_Uin_from_Uquest.compute(Uquest, a)

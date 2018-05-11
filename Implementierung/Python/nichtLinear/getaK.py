# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 11:22:44 2017

@author: denys
"""
def get(U_out, N, toPlot):

    import getH
    import computea
    import numpy as np
    from Helpers import writeAWG, writeDSO
    import computeU_out_to_U_quest

    samplerateAWG = 999900000


    def sendUinToAWG(U_in):

        awg_volt=200e-3 #Vpp die das awg ausgeben soll
        writeAWG(U_quest, samplerateAWG, awg_volt)

    def receiveUqeust(U_quest):

        fmax = 80e6
        samplerateOszi = 100 * samplerateAWG
        vpp = 200e-3
        [time, dataUin, dataUout] = writeDSO.writeDSO(samplerateOszi, vpp, fmax, U_quest)

        return(time, dataUin, dataUout)


    [frq, H, PhaseH] = getH.compute(80e6, 40e-3, 10, True, True, True, 1, False)

    U_in = computeU_out_to_U_quest.compute(U_out, H)

    sendUinToAWG(U_in)

    U_quest = receiveUqeust()

    in_pp = max(U_in) - min(U_in)

    [a, K] = computea.compute(U_in, in_pp, U_quest, N, toPlot)

    return(a, K)
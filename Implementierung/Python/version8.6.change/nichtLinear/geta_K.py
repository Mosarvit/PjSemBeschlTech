# -*- coding: utf-8 -*-
"""
Created on Thu Jul 13 11:22:44 2017

@author: denys
"""
def get(Uout, N, toPlot):

    import get_H
    from compute import compute_a_from_Uin_Uquet
    from helpers import writeAWG, writeDSO
    from compute import compute_Uquest_from_Uout

    samplerateAWG = 999900000


    def sendUinToAWG(Uin):

        awg_volt=200e-3 #Vpp die das awg ausgeben soll
        writeAWG(Uquest, samplerateAWG, awg_volt)

    def receiveUqeust(Uquest):

        fmax = 80e6
        samplerateOszi = 100 * samplerateAWG
        vpp = 200e-3
        [time, dataUin, dataUout] = writeDSO.writeDSO(samplerateOszi, vpp, fmax, Uquest)

        return(time, dataUin, dataUout)


    [frq, H, PhaseH] = get_H.get(80e6, 40e-3, 10, True, True, True, 1, False)

    Uin = compute_Uquest_from_Uout.compute(Uout, H)

    sendUinToAWG(Uin)

    Uquest = receiveUqeust()

    in_pp = max(Uin) - min(Uin)

    [a, K] = compute_a_from_Uin_Uquet.compute(Uin, in_pp, Uquest, N, toPlot)

    return(a, K)
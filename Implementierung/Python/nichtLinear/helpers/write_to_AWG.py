# -*- coding: utf-8 -*-
"""

"""


def send(signal, samplerateAWG, awg_volt):
    import visa
    from helpers import MLBS
    import time
    import matplotlib.pyplot as plt
    import numpy as np
    from helpers import FFT
    import csv
    import os

    if awg_volt > 0.8 :
        raise ValueError('The voltage is too high for the amplifier, should not be higher than 0.8 ! ')
    else :

        # Connect to Instruments
        rm = visa.ResourceManager()
        rs = rm.list_resources()
        for i in range(0, len(rs)):
            pruf = rs[i]
            test = pruf.find("USB")
            if test != -1:
                index = i
        awg_id = rs[index]
        AWG = rm.open_resource(awg_id)
        AWG.write("*RST")
        AWG.write("SOURce1:FUNCtion:ARBitrary:FILTer OFF")
        AWG.write("SOURce2:FUNCtion:ARBitrary:FILTer OFF")
        # time.sleep(5)
        AWG.write("DATA:VOLatile:CLEar")
        # time.sleep(5)
        myrange = max(abs(max(signal)), abs(min(signal)))
        # Data Conversion from V to DAC levels
        data_conv = np.round(signal * 32766 / myrange);
        # with open(directory + '/csv/arbin.csv', 'w', newline="") as csvfile:
        #     writer = csv.writer(csvfile, delimiter=';',
        #                         quotechar='|', quoting=csv.QUOTE_MINIMAL)
        #     for i in range(0, data_conv.size):
        #         writer.writerow([str(data_conv[i])])
        data_conv = ",".join(str(e) for e in data_conv)
        AWG.write("SOURce1:DATA:ARBitrary:DAC myarb ," + data_conv)
        AWG.write("SOURce1:FUNCtion:ARBitrary 'myarb'")
        time.sleep(10)
        AWG.write("SOURce1:FUNCtion ARB")  # USER
        AWG.write("DISPlay:FOCus CH1")
        AWG.write("DISPlay:UNIT:ARBRate FREQuency")
        AWG.write("SOURce1:FUNCtion:ARBitrary:SRATe " + str(samplerateAWG))
        AWG.write("SOURce2:DATA:ARBitrary:DAC myarb ," + data_conv)
        AWG.write("SOURce2:FUNCtion:ARBitrary 'myarb'")
        time.sleep(10)
        AWG.write("SOURce2:FUNCtion ARB")  # USER
        AWG.write("DISPlay:FOCus CH2")
        AWG.write("DISPlay:UNIT:ARBRate FREQuency")
        AWG.write("SOURce2:FUNCtion:ARBitrary:SRATe " + str(samplerateAWG))
        AWG.write("FUNC:ARB:SYNC")
        AWG.write("SOURce1:VOLTage " + str(awg_volt))
        AWG.write("SOURce2:VOLTage " + str(awg_volt))
        time.sleep(5)
        AWG.write("OUTPut1 ON")
        AWG.write("OUTPut2 ON")
        AWG.write("DISPlay:FOCus CH1")
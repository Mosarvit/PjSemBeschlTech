# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 10:28:22 2017

@author: denys
"""
def writeAWG(signal, samplerateAWG, awg_volt):
    import visa
    import numpy as np
    import time
    
    
    # Connect to Instruments
    rm = visa.ResourceManager()
    rs = rm.list_resources()
    for i in range (0,len(rs)):
        pruf=rs[i]
        test=pruf.find("USB")
        if test != -1:
            index=i
    awg_id = rs[index]
    AWG = rm.open_resource(awg_id)
    
    ##################################################
    ################## Write to AWG ##################
    ##################################################
    
    AWG.write("*RST") 
    #time.sleep(5)
    AWG.write("DATA:VOLatile:CLEar")
    #time.sleep(5)
    myrange=max(abs(max(signal)),abs(min(signal)))
     #Data Conversion from V to DAC levels
    data_conv = np.round(signal*32766/myrange);  
    data_conv = ",".join(str(e) for e in data_conv)
    AWG.write("SOURce1:DATA:ARBitrary:DAC myarb ," + data_conv)
    time.sleep(10)
    AWG.write("SOURce1:FUNCtion:ARBitrary 'myarb'")
    time.sleep(10)
    AWG.write("SOURce1:FUNCtion ARB") #USER
    AWG.write("DISPlay:FOCus CH1")
    AWG.write("DISPlay:UNIT:ARBRate FREQuency")
    AWG.write("SOURce1:FUNCtion:ARBitrary:SRATe " + str(samplerateAWG))
    AWG.write("SOURce2:DATA:ARBitrary:DAC myarb ," + data_conv)
    AWG.write("SOURce2:FUNCtion:ARBitrary 'myarb'")
    time.sleep(10)
    AWG.write("SOURce2:FUNCtion ARB") #USER
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
   
    return (signal, samplerateAWG, awg_volt)
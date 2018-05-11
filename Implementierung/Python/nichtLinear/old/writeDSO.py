# -*- coding: utf-8 -*-
"""
Created on Wed Dec 20 10:43:54 2017

@author: denys
"""
def writeDSO(samplerateOszi, awg_volt, fmax, signal):
    import visa
    import numpy as np
    import time
    

    dso_ip = 'TCPIP::169.254.225.181::gpib0,1::INSTR'
    DSO = visa.ResourceManager().get_instrument(dso_ip)
    
    Tns = 0.4/fmax
    periodTime = signal.size*Tns
    horizontalScalePerDiv = 1.5*periodTime/10 #At least one period needs to be
                                              #shown on the DSO 
    
    possibleRecordLength = [500,2500,5000,10e3,25e3,50e3,100e3,250e3,500e3]
    possibleRecordLength = np.array(possibleRecordLength)
    
    ##WRITE DSO
    DSO.write("*RST") #Restores the state of the instrument from a copy of 
                      #the settings stored in memory
    DSO.write("ACQUIRE:STATE OFF") #This command stops acquisitions
    DSO.write("SELECT:CH1 ON") #Turns the channel 1 waveform display on, and
                               #selects channel 1.
    DSO.write("MATH3:DEFIne \"CH3-CH4\"") #Defines MATH function
            
    DSO.write("SELECT:MATH3 ON") #Turns MATH3 display on
    DSO.write("MATH1:DEFIne \"CH1\"") #Defines MATH function. CH1 is copied
                                        #to MATH1, because output format of
                                        #MATH1 is easier to handle
    DSO.write("SELECT:MATH1 ON") #Turns MATH1 display on
    DSO.write("TRIGger:A:EDGE:SOUrce CH1") #This command sets or queries the 
                                           #source for the A edge trigger.
    DSO.write("TRIGger:A:EDGE:SLOpe FALL") #This command sets or queries the 
                                           #slope for the A edge trigger.
                                           
    DSO.write("HORizontal:MAIn:SCAle " + str(horizontalScalePerDiv)) #Sets the 
    #time per division for the time base
    # Here 1,5 periods are on screen. Necessary since Osci has only discrete
    # values for horizontal scale and it needs to be ensured that at least
    # one full period is in the screen        
    horizontalScalePerDiv = DSO.query("HORizontal:MAIn:SCAle?")
    horizontalScalePerDiv = [float(s) for s 
                             in horizontalScalePerDiv.split(',')] 
    horizontalScalePerDiv = horizontalScalePerDiv[0]
    recordLength = horizontalScalePerDiv*10*samplerateOszi
    ind = np.argmin(np.abs(recordLength - possibleRecordLength))
    if possibleRecordLength[ind] < recordLength and \
    (ind+1)<possibleRecordLength.size:
        recordLength = possibleRecordLength[ind+1]
    else:
        recordLength = possibleRecordLength[ind]
    DSO.write("HORIZONTAL:RECOrdlength " + str(recordLength)) #1e5
    DSO.write("CH1:SCAle " + str(awg_volt/6)) #Sets the vertical scale
    DSO.write("MATH1:SCAle " + str(awg_volt/6)) #Sets the vertical scale
    DSO.write("CH2:SCAle 20.0E-3") #Sets the vertical scale 
    DSO.write("CH3:SCAle " + str(awg_volt*10)) #Sets the vertical scale 
    DSO.write("CH4:SCAle " + str(awg_volt*10)) #Sets the vertical scale
    DSO.write("MATH3:SCAle " + str(awg_volt*50)) #Sets the vertical scale       
    
    DSO.write("CH1:POSition 0") #Sets the horizontal scale
    DSO.write("MATH3:POSition 0") #Sets the horizontal scale
    DSO.write("MATH1:POSition 0") #Sets the horizontal scale
    DSO.write("CH1:TERmination 1.0E+6") #Sets the termination of the channel
    DSO.write("CH2:TERmination 1.0E+6") #Sets the termination of the channel
    DSO.write("CH3:TERmination 1.0E+6") #Sets the termination of the channel
    DSO.write("CH4:TERmination 1.0E+6") #Sets the termination of the channel
    DSO.write("CH1:COUPling DC")  #Sets the coupling of channel 1 to AC
    # Coupling to AC since the input signal has no DC component.
    # No DC expected at the output. Use AC coupling to reduce influence
    # from outside.
    DSO.write("DATa:SOUrce MATH1")   #This command sets the location of
                                   #waveform data that is transferred from the
                                   #instrument by the CURVe? Query
    DSO.write("DATa:ENCdg ASCIi") #This command sets the format of outgoing
                                  #waveform data to ASCII 
    DSO.write("ACQUIRE:MODE SAMPLE") #This command sets the acquisition mode
                                     #of the instrument to sample mode 
    DSO.write("ACQUIRE:STOPAFTER SEQUENCE") #Specifies that the next
                                            #acquisition will be a 
                                            #single-sequence acquisition.
    DSO.write("HORizontal:MAIn:SAMPLERate " + str(samplerateOszi)) # Sets the 
                                            # sample rate of the device.
                                            # Here: 10 times maximum expected 
                                            # frequency to reduce aliasing                               
    DSO.write("ACQUIRE:STATE ON") #This command starts acquisitions
    DSO.write("DATa:STARt 1") #This command sets the starting data point 
                    #for waveform transfer. This command allows for the 
                    #transfer of partial waveforms to and from the instrument.
    DSO.write("DATa:STOP " + DSO.query("HORIZONTAL:RECOrdlength?")) #Sets the
       #last data point that will be transferred when using the CURVe? query
    time.sleep(5)
    dataUin = DSO.query("CURVe?")
    DSO.write("DATa:SOUrce MATH3")   #This command sets the location of
                                   #waveform data that is transferred from the
                                   #instrument by the CURVe? Query
    DSO.write("DATa:ENCdg ASCIi") #This command sets the format of outgoing 
                                  #waveform data to ASCII 
    DSO.write("DATa:STARt 1") #This command sets the starting data point 
                    #for waveform transfer. This command allows for the
                    #transfer of partial waveforms to and from the instrument.
    DSO.write("DATa:STOP " + DSO.query("HORIZONTAL:RECOrdlength?")) #Sets the
         #last data point that will be transferred when using the CURVe? query
    time.sleep(5)
    dataUout = DSO.query("CURVe?")
    
    recordLength = DSO.query("HORIZONTAL:RECOrdlength?")
    horizontalScalePerDiv = DSO.query("HORizontal:MAIn:SCAle?")
    YScalePerDivUin = DSO.query("MATH1:SCAle?")
    YScalePerDivUout = DSO.query("MATH3:SCAle?")
    
        # Change format of data from DSO
    dataUin = [float(s) for s in dataUin.split(',')]
    
    dataUout = [float(s) for s in dataUout.split(',')]
    dataUin = np.array(dataUin)
    dataUout = np.array(dataUout)
    recordLength = [float(s) for s in recordLength.split(',')]  
    recordLength = recordLength[0]        
    horizontalScalePerDiv = [float(s) for s 
                             in horizontalScalePerDiv.split(',')]  
    horizontalScalePerDiv = horizontalScalePerDiv[0]
    YScalePerDivUin = [float(s) for s in YScalePerDivUin.split(',')]  
    YScalePerDivUin = YScalePerDivUin[0]
    YScalePerDivUout = [float(s) for s in YScalePerDivUout.split(',')]  
    YScalePerDivUout = YScalePerDivUout[0]
    
    # Get time vector
    dt = 10*horizontalScalePerDiv/recordLength
    time = np.arange(0,10*horizontalScalePerDiv,dt)
    
    # Reduce time vector and signal to one period, this only holds for the MLBS Signal
    tmpTime = periodTime - time[0]
    ind = np.argmin(abs(time - tmpTime)) #find next index
    time = time[0:ind]
    dataUin = dataUin[0:ind]
    dataUout = dataUout[0:ind]
    
    return (time, dataUin, dataUout)
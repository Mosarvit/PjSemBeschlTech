# -*- coding: utf-8 -*-


def read(samplerateOszi, vpp_ch1, vpp_out, fmax, signal, measure_H = False):

    """

    read_from_DSO liest das Eingagns- und Ausgangssignal aus DSO ein

    INPUT:

        awg_volt : skalar; Output peak-peak voltage of the signal
        samplerateOszi: positiver integer; Abtastrate des DSO
        fmax : positiver skalar; max frequency of interest
        signal : nx1 vector; Signalvektor
        measure_H : set true for measure H with Denys method

    OUTPUT:

        time : nx1 vector; Zeitvektor
        dataUin : nx1 vector; Signalvektor des Eingangssignals (Vorausgesetzt richtig angeschlossen ans DSO)
        dataUout : nx1 vector; Signalvektor des Eingangssignals (Vorausgesetzt richtig angeschlossen ans DSO)
        :param measure_H:

    """

    import visa
    import numpy as np
    import time
    from settings import f_rep

    dso_ip = 'TCPIP::169.254.225.181::gpib0,1::INSTR'
    DSO = visa.ResourceManager().get_instrument(dso_ip)
    if measure_H:
        Tns = 0.4/fmax
        periodTime = signal.size*Tns
        horizontalScalePerDiv = 1.5*periodTime/10 #At least one period needs to be
                                                  #shown on the DSO 
    else:
        # f_rep from global settings
        periodTime = 1/f_rep
        horizontalScalePerDiv = 1.5*periodTime/10
    
    # random samplerate versuch max
    samplerateAWG = 2.5*fmax
    samplerateOszi = 100*samplerateAWG
    
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
    # MN: Meine Vermutung: Skalierung pro Division.
    # MN: Eigentlich sind 8 Divisionen vorhaden; Vpp wird durch 6 geteilt -> Sicherheitsabstand
    DSO.write("CH1:SCAle " + str(vpp_ch1 / 6)) #Sets the vertical scale
    DSO.write("MATH1:SCAle " + str(vpp_ch1 / 6)) #Sets the vertical scale
    version = 2
    if version == 1:
        DSO.write("CH2:SCAle 20.0E-3") #Sets the vertical scale 
        DSO.write("CH3:SCAle 50.0E-3") #Sets the vertical scale 
        DSO.write("CH4:SCAle 50.0E-3") #Sets the vertical scale
        DSO.write("MATH3:SCAle 200.0E-3") #Sets the vertical scale
    elif version == 2:
        DSO.write("CH2:SCAle 20.0E-3") #Sets the vertical scale
        DSO.write("CH3:SCAle " + str(vpp_out / 4)) #Sets the vertical scale
        DSO.write("CH4:SCAle " + str(vpp_out / 4)) #Sets the vertical scale
        # MN: Hier muss glaube ich der Faktor 1/2 hin, weil die Amplitude gemeint ist
        DSO.write("MATH3:SCAle " + str(vpp_out / 2)) #Sets the vertical scale
    
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
    samplerate_initial = DSO.query("HORizontal:MAIn:SAMPLERate?")
    DSO.write("HORizontal:MAIn:SAMPLERate " + str(samplerateOszi)) # Sets the 
                                            # sample rate of the device.
                                            # Here: 10 times maximum expected 
                                            # frequency to reduce aliasing 
    samplerate_new = DSO.query("HORizontal:MAIn:SAMPLERate?")
    DSO.write("ACQUIRE:STATE ON") #This command starts acquisitions
    DSO.write("DATa:STARt 1") #This command sets the starting data point 
                    #for waveform transfer. This command allows for the 
                    #transfer of partial waveforms to and from the instrument.
    DSO.write("DATa:STOP " + DSO.query("HORIZONTAL:RECOrdlength?")) #Sets the
       #last data point that will be transferred when using the CURVe? query

    time_attempt = 1        #chooses version to wait for finishing commands
    if time_attempt == 1:
        time.sleep(5)       #enough time to finish every Process
    elif time_attempt == 2:
        DSO.query("*OPC?")  #new attempt 1 to reduce time to wait -> does not proceed until *OPC? is set to 1 by internal queue.
                        # so, finishing this line in the program will last until the device is ready
                        # In case this is not working, try DSO.write("*OPC?") instead, just as a guess
                        # can used as a boolean variable, finished = DSO.query("*OPC?"), if necessary for a loop
    elif time_attempt == 3:
        busy = DSO.query("BUSY?")          #new attempt 2 to reduce time to wait -> runs until OPC? is set to 1
        while busy=="1":                        #loop until not busy any more
               time.sleep(0.01)         #just to pose less requests to DSO, 10 msec waiting time -> not necessary
               busy = DSO.query("BUSY?")
               print(busy)                 #just to have a control option -> not necessary, it an attempt work
                                        # In case this is not working, try DSO.write("BUSY") instead, just as a guess
    else :
        DSO.write("*WAI")   #new attempt 3 to reduce time to wait -> DSO will wait till commands above are finished.
                            # python will go on and write the commands in the input buffer
                            # they will be executed after WAI has finished
    # new attempt 3 and another not named attempt are possible, but 1 and 2 are faster and more stable

    dataUin = DSO.query("CURVe?")
    DSO.write("DATa:SOUrce MATH3")   #This command sets the location of
                                   #waveform data that is transferred from the
                                   #instrument by the CURVe? Query
    DSO.write("DATa:ENCdg ASCIi") #This command sets the format of outgoing 
                                  #waveform data to ASCII 
    DSO.write("DATa:STARt 1") #This command sets the starting data point 
                    #for wavefosrm transfer. This command allows for the
                    #transfer of partial waveforms to and from the instrument.
    DSO.write("DATa:STOP " + DSO.query("HORIZONTAL:RECOrdlength?")) #Sets the
         #last data point that will be transferred when using the CURVe? query

    time_attempt = 2  # chooses version to wait for finishing commands
    if time_attempt == 1:
        time.sleep(5)  # enough time to finish every Process -> original implementation
    elif time_attempt == 2:
        DSO.query("*OPC?")  # new attempt 1 to reduce time to wait -> does not proceed until *OPC? is set to 1 by internal queue.
        # so, finishing this line in the program will last until the device is ready
        # In case this is not working, try DSO.write("*OPC?") instead, just as a guess
        # can used as a boolean variable, finished = DSO.query("*OPC?"), if necessary for a loop
    elif time_attempt == 3:
        busy = DSO.query("BUSY?")  # new attempt 2 to reduce time to wait -> runs until OPC? is set to 1
        while busy=='1':  # loop until not busy any more
            time.sleep(0.01)  # just to pose less requests to DSO, 10 msec waiting time -> not necessary
            busy = DSO.query("BUSY?")
            print(busy)  # just to have a control option -> not necessary, it an attempt work
            # In case this is not working, try DSO.write("BUSY") instead, just as a guess
    else:
        DSO.write("*WAI")  # new attempt 3 to reduce time to wait -> DSO will wait till commands above are finished.
        # python will go on and write the commands in the input buffer
        # they will be executed after WAI has finished
    # new attempt 3 and another not named attempt are possible, but 1 and 2 are faster and more stable

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
    ind = ind + 1
    offset = 12500
    time = time[0:ind]
    dataUin = dataUin[offset + 0:offset + ind]
    dataUout = dataUout[offset + 0:offset + ind]
    
    return (time, dataUin, dataUout)
# -*- coding: utf-8 -*-
"""

"""


def write_to_AWG(signal, samplerateAWG, awg_volt):

    """

    write_to_AWG sendet ein Singal an den AWG

    INPUT:

        awg_volt : skalar; Output peak-peak voltage of AWG
        samplerateAWG: positiver integer; Abtastrate des AWG
        signal : nx1 vector; Signalvektor

    OUTPUT:

        (no output)

    """

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
        
        time_attempt = 1  # chooses version to wait for finishing commands
        if time_attempt == 1:
            time.sleep(5)  # enough time to finish every Process -> original implementation
        elif time_attempt == 2:
            AWG.write("*OPC?")  # new attempt 1 to reduce time to wait
            # -> does not proceed until *OPC? is set to 1 by internal queue.
            # so, finishing this line in the program will last until the device is ready
            # In case this is not working, try AWG.write("*OPC?") instead, just as a guess
            # can used as a boolean variable, finished = AWG.query("*OPC?"), if necessary for a loop
        elif time_attempt == 3:
            AWG.write("*WAI")  # new attempt 2 to reduce time to wait -> AWG will wait till commands above are finished.
            # python will go on and write the commands in the input buffer
            # they will be executed after WAI has finished
        # new attempt 2 and another not named attempt are possible, but 1 is faster and more stable
        else :
            time.sleep(1.3)  #attempt 3 to reduce time to wait
            # -> see data sheet: maximum time needed to write is given by 1.25 sec
            
        AWG.write("SOURce1:FUNCtion:ARBitrary 'myarb'")

        time_attempt = 1  # chooses version to wait for finishing commands
        if time_attempt == 1:
            time.sleep(5)  # enough time to finish every Process -> original implementation
        elif time_attempt == 2:
            AWG.query("*OPC?")  # new attempt 1 to reduce time to wait
            # -> does not proceed until *OPC? is set to 1 by internal queue.
            # so, finishing this line in the program will last until the device is ready
            # In case this is not working, try AWG.write("*OPC?") instead, just as a guess
            # can used as a boolean variable, finished = AWG.query("*OPC?"), if necessary for a loop
        elif time_attempt == 3:
            AWG.write("*WAI")  # new attempt 2 to reduce time to wait -> AWG will wait till commands above are finished.
            # python will go on and write the commands in the input buffer
            # they will be executed after WAI has finished
        # new attempt 2 and another not named attempt are possible, but 1 is faster and more stable
        else :
            time.sleep(1.3)  #attempt 3 to reduce time to wait
            # -> see data sheet: maximum time needed to write is given by 1.25 sec

        AWG.write("SOURce1:FUNCtion ARB")  # USER
        AWG.write("DISPlay:FOCus CH1")
        AWG.write("DISPlay:UNIT:ARBRate FREQuency")
#        AWG.write("SOURce1:FUNCtion:ARBitrary:SRATe " + str(samplerateAWG))
#        AWG.query("SOURce1:FUNCtion:ARBitrary:SRATe? ")
        AWG.write("SOURce1:FUNCtion:ARBitrary:FREQ " + str(900000))
#        AWG.query("SOURce1:FUNCtion:ARBitrary:FREQ?")
        
        time_attempt = 1  # chooses version to wait for finishing commands
        if time_attempt == 1:
            time.sleep(5)  # enough time to finish every Process -> original implementation
        elif time_attempt == 2:
            AWG.write("*OPC?")  # new attempt 1 to reduce time to wait
            # -> does not proceed until *OPC? is set to 1 by internal queue.
            # so, finishing this line in the program will last until the device is ready
            # In case this is not working, try AWG.write("*OPC?") instead, just as a guess
            # can used as a boolean variable, finished = AWG.query("*OPC?"), if necessary for a loop
        elif time_attempt == 3:
            AWG.write("*WAI")  # new attempt 2 to reduce time to wait -> AWG will wait till commands above are finished.
            # python will go on and write the commands in the input buffer
            # they will be executed after WAI has finished
        # new attempt 2 and another not named attempt are possible, but 1 is faster and more stable
        elif time_attempt == 4:
            busy = AWG.write("BUSY?")  # new attempt 2 to reduce time to wait -> runs until OPC? is set to 1
            print("busy:")    
            print(busy)
            print("busy ready")
            while busy=='1':  # loop until not busy any more
                time.sleep(0.01)  # just to pose less requests to DSO, 10 msec waiting time -> not necessary
                busy = AWG.query("BUSY?")
                print(busy)  # just to have a control option -> not necessary, it an attempt work
                # In case this is not working, try DSO.write("BUSY") instead, just as a guess
        
        
        else:
            time.sleep(1.3)  # attempt 3 to reduce time to wait
            # -> see data sheet: maximum time needed to write is given by 1.25 sec

        AWG.write("SOURce2:DATA:ARBitrary:DAC myarb ," + data_conv)
        
        time_attempt = 1  # chooses version to wait for finishing commands
        if time_attempt == 1:
            time.sleep(5)  # enough time to finish every Process -> original implementation
        elif time_attempt == 2:
            AWG.query("*OPC?")  # new attempt 1 to reduce time to wait
            # -> does not proceed until *OPC? is set to 1 by internal queue.
            # so, finishing this line in the program will last until the device is ready
            # In case this is not working, try AWG.write("*OPC?") instead, just as a guess
            # can used as a boolean variable, finished = AWG.query("*OPC?"), if necessary for a loop
        elif time_attempt == 3:
            AWG.write("*WAI")  # new attempt 2 to reduce time to wait -> AWG will wait till commands above are finished.
            # python will go on and write the commands in the input buffer
            # they will be executed after WAI has finished
        # new attempt 2 and another not named attempt are possible, but 1 is faster and more stable
        else:
            time.sleep(1.3)  # attempt 3 to reduce time to wait
            # -> see data sheet: maximum time needed to write is given by 1.25 sec

        AWG.write("SOURce2:FUNCtion:ARBitrary 'myarb'")

        time_attempt = 1  # chooses version to wait for finishing commands
        if time_attempt == 1:
            time.sleep(5)  # enough time to finish every Process -> original implementation
        elif time_attempt == 2:
            AWG.query("*OPC?")  # new attempt 1 to reduce time to wait
            # -> does not proceed until *OPC? is set to 1 by internal queue.
            # so, finishing this line in the program will last until the device is ready
            # In case this is not working, try AWG.write("*OPC?") instead, just as a guess
            # can used as a boolean variable, finished = AWG.query("*OPC?"), if necessary for a loop
        elif time_attempt == 3:
            AWG.write("*WAI")  # new attempt 2 to reduce time to wait -> AWG will wait till commands above are finished.
            # python will go on and write the commands in the input buffer
            # they will be executed after WAI has finished
        # new attempt 2 and another not named attempt are possible, but 1 is faster and more stable
        else:
            time.sleep(1.3)  # attempt 3 to reduce time to wait
            # -> see data sheet: maximum time needed to write is given by 1.25 sec

        AWG.write("SOURce2:FUNCtion ARB")  # USER
        AWG.write("DISPlay:FOCus CH2")
        AWG.write("DISPlay:UNIT:ARBRate FREQuency")
#        AWG.write("SOURce2:FUNCtion:ARBitrary:SRATe " + str(samplerateAWG))
#        AWG.query("SOURce2:FUNCtion:ARBitrary:SRATe? ")
        AWG.write("SOURce2:FUNCtion:ARBitrary:FREQ " + str(900000))
#        AWG.write("SOURce2:FUNCtion:ARBitrary:FREQ?")
        AWG.write("FUNC:ARB:SYNC")
        AWG.write("SOURce1:VOLTage " + str(awg_volt))
        AWG.write("SOURce2:VOLTage " + str(awg_volt))

        time_attempt = 1  # chooses version to wait for finishing commands
        if time_attempt == 1:
            time.sleep(5)  # enough time to finish every Process -> original implementation
        elif time_attempt == 2:
            AWG.query("*OPC?")  # new attempt 1 to reduce time to wait
            # -> does not proceed until *OPC? is set to 1 by internal queue.
            # so, finishing this line in the program will last until the device is ready
            # In case this is not working, try AWG.write("*OPC?") instead, just as a guess
            # can used as a boolean variable, finished = AWG.query("*OPC?"), if necessary for a loop
        elif time_attempt == 3:
            AWG.write("*WAI")  # new attempt 2 to reduce time to wait -> AWG will wait till commands above are finished.
            # python will go on and write the commands in the input buffer
            # they will be executed after WAI has finished
        # new attempt 2 and another not named attempt are possible, but 1 is faster and more stable
        else:
            time.sleep(1.3)  # attempt 3 to reduce time to wait
            # -> see data sheet: maximum time needed to write is given by 1.25 sec

        AWG.write("OUTPut1 ON")
        AWG.write("OUTPut2 ON")
        AWG.write("DISPlay:FOCus CH1")
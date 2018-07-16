# -*- coding: utf-8 -*-
"""
    This implementation is based on the work of Denys and Armin
    Expanded by setting the frequency and handling errors
"""

import visa
import time
import numpy as np
from classes import signal_class
from helpers import FFT
import os

def write_to_AWG(signal, awg_Vpp, samplerateAWG=0, frequency=0):

    """
    write_to_AWG sends the described signal to the AWG s.t. it is send by both of the AWG's channels
    Used for Keysight Trueform 336_2A, USB-Remote controlled (via USB Port 1 of Laptop)
    The function uses the global vertical resolution of the AWG with 32766 samples ( 15 bit)

    The function can handle either the sample-rate OR the frequency of the given Signal.
    With sample-rate: calculating the frequency by using the number of data points in the signal
    With frequency: repeat-frequency of the given signal

    The function does not track one channel to the other but writes the same parameters to both channels.

    Built-in safety:
        - only Vpp up to 0.8 Volt are supported due to the use of this code in the context of a Barrier-Bucket-System
            with a voltage-amplifier with a maximum input voltage Vpp of approximately 1 V.
            This value was not extracted from the handbook! If necessary, do further research.
        -

    (Function reads out errors of the AWG and stops continuing the code with an exception.
    Function requests the AWG to highlight when a command is fully executed.
    There are different possible attempts, in case one is not working.)

    :param signal: an array of size n x 1
    :param awg_Vpp: the max peak-to-peak voltage (in V) of the signal used for normalizing the signal,
                        positive scalar value
    :param samplerateAWG: the number of samples the AWG has to send in a second (excluding frequency),
                        positive scalar value
    :param frequency: the repetition rate of the signal, number of repetitions in a second in Hz
                        (excluding samplerateAWG), positive scalar value
    :return: (no output)

    """

    # TODO: wait for AWG after each (nontrivial) command if possible with *OPC?
    # TODO: check for erros (see evaluate connect devices) and throw exceptions

    type_check_write_AWG(signal, awg_Vpp, samplerateAWG, frequency)

    # built-in safety: maximum Vpp is 0.8 Volt to avoid damage to the amplifier
    if awg_Vpp > 0.8:
        raise ValueError('The voltage is too high for the amplifier, should not be higher than 0.8 ! ')
    else:

        if (frequency != 0) and (samplerateAWG != 0):
            raise ValueError('Frequency and samplerate can not both be send to the AWG')

        vertical_resolution = 32766

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

        # restore the instrument and set filters off to avoid smoothing data
        AWG.write("*RST")
        AWG.write("SOURce1:FUNCtion:ARBitrary:FILTer OFF")
        AWG.write("SOURce2:FUNCtion:ARBitrary:FILTer OFF")
        AWG.write("DATA:VOLatile:CLEar")

        # Data Conversion from V to DAC levels
        myrange = max(abs(max(signal)), abs(min(signal)))
        data_conv = np.round(signal * vertical_resolution / myrange)
        data_conv = ",".join(str(e) for e in data_conv)
        AWG.write("SOURce1:DATA:ARBitrary:DAC myarb ," + data_conv)
        
        time_attempt = 1  # chooses version to wait for finishing commands
        wait_for_AWG(AWG, 0) # TODO check, then delete the following and replace 0 with time_attempt
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
        wait_for_AWG(AWG, 0) # TODO check, then delete the following and replace 0 with time_attempt
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

        AWG.write("SOURce1:FUNCtion ARB")  # change to user-defined function
        AWG.write("DISPlay:FOCus CH1")
        AWG.write("DISPlay:UNIT:ARBRate FREQuency")
        if samplerateAWG != 0:
            AWG.write("SOURce1:FUNCtion:ARBitrary:SRATe " + str(samplerateAWG))
        else:
            AWG.write("SOURce1:FUNCtion:ARBitrary:FREQ " + str(frequency))

        time_attempt = 1  # chooses version to wait for finishing commands
        wait_for_AWG(AWG, 0) # TODO check, then delete the following and replace 0 with time_attempt
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
        wait_for_AWG(AWG, 0) # TODO check, then delete the following and replace 0 with time_attempt
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
        wait_for_AWG(AWG, 0) # TODO check, then delete the following and replace 0 with time_attempt
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
        if samplerateAWG != 0:
            AWG.write("SOURce1:FUNCtion:ARBitrary:SRATe " + str(samplerateAWG))
        else:
            AWG.write("SOURce1:FUNCtion:ARBitrary:FREQ " + str(frequency))

        AWG.write("FUNC:ARB:SYNC")
        AWG.write("SOURce1:VOLTage " + str(awg_Vpp))
        AWG.write("SOURce2:VOLTage " + str(awg_Vpp))

        time_attempt = 1  # chooses version to wait for finishing commands
        wait_for_AWG(AWG, 0) # TODO check, then delete the following and replace 0 with time_attempt
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

        # turn both channels on
        AWG.write("OUTPut1 ON")
        AWG.write("OUTPut2 ON")
        AWG.write("DISPlay:FOCus CH1")

        return

def type_check_write_AWG(signal, awg_Vpp, samplerateAWG, frequency):
    """
    This method handles the input checks for write_to_AWG s.t. it is clear where problems are ocurring.
    See documentation of write_to_AWG for detailed information about the used type-checks.

    :param signal: an array of size n x 1 - no input check necessary (July 18)
    :param awg_Vpp: the max peak-to-peak voltage (in V) of the signal used for normalizing the signal, positive scalar value
    :param samplerateAWG: the number of samples the AWG has to send in a second (excluding frequency), positive scalar value
    :param frequency: the repetition rate of the signal, number of repetitions in a second (excluding samplerateAWG), positive scalar value
    :return: (no output)
    """

    if awg_Vpp > 0.8:
        raise ValueError('The voltage is too high for the amplifier, should not be higher than 0.8 ! ')

    if frequency < 0:
        raise ValueError('Frequency has to be positive')
    if samplerateAWG <0:
        raise ValueError('Samplerate has to be positive')
    if (frequency != 0) and (samplerateAWG != 0):
        raise ValueError('Frequency and samplerate can not both be send to the AWG')
    # if samplerateAWG > max_samplerate_awg: # requires check for highest samplerate first (datasheet)
    #     raise ValueError('Samplerate is too high: for Keysighnt 3362_A is Rate max ' + str(max_samplerate_awg))

    return


def wait_for_AWG(AWG, attempt=0):
    """

    :param AWG: the Signal Generator to wait for, - designed by visa resourcemanager open
    :param attempt: choice of which wait-routine to run
    :return: no output
    """

    if attempt == 1:
        time.sleep(1.3)  # simple to reduce time to wait
        # -> see data sheet: maximum time needed to write data is given by 1.25 sec for large signals and USB control
    elif attempt == 2:
        AWG.query("*OPC?")  # new attempt to reduce time to wait
        # -> does not proceed until *OPC? is set to 1 by internal queue.
        # so, finishing this line in the program will last until the device is ready
        # In case this is not working, try AWG.write("*OPC?") and AWG.read() instead, which should be the same.
        # (see pyvisa-documentation for more information)
        # can used as a boolean variable, finished = AWG.query("*OPC?"), if necessary for a loop
    elif attempt == 3:
        AWG.write("*WAI")  # new attempt  to reduce time to wait -> AWG will wait till commands above are finished.
        # python will go on and write the commands in the input buffer
        # they will be executed after WAI has finished
        # this attempt and the following are possible, but attempt 2 should be faster and more stable
    elif attempt == 4:
        busy = AWG.write("BUSY?")  # new attempt to reduce time to wait -> runs until OPC? is set to 1
        print("busy:") # just as a control output
        print(busy)
        print("busy ready")
        while busy == '1':  # loop until not busy any more
            time.sleep(0.01)  # just to pose less requests to DSO, 10 msec waiting time -> not necessary
            busy = AWG.query("BUSY?")
            print(busy)  # just to have a control option -> not necessary
    else:
        time.sleep(5)  # enough time to finish every Process -> original implementation, loooong run-time
    return
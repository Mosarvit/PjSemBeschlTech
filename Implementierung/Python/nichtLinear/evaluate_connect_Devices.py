"""
    This module offers checks for the devices used in the context of the barrier bucket systems, which are:
    (July 2018)
    - AWG Keysight via USB
    - Tektronix DSO via Lan

    The advantage of this module is that it is not necessary to start the main routine
    and be surprised by errors thrown there.
    This is like a developer mode for new ideas before doing changes in the main routine, especially in
    - write_to_AWG.write
    - read_from_DSO.read
"""

import visa
import time
import matplotlib.pyplot as plt
import numpy as np
import timeit
from blocks.generate_BBsignal import generate_BBsignal


# TODO: wait for AWG / DSO after each (nontrivial) command if possible with *OPC? after checking time-attempts


def check_AWG():
    """
    checks whether the AWG is connected correctly before starting the program to avoid program mistakes in functionality running.
    Especially enables to check code to communicate withe the AWG like the run-time optimization.

    OUTPUT:

        (no output)

    """

    # Define functions to use time-analysis by timeit.timeit
    # TODO: find clever solution instead of the following, ugly implementation for measuring the run-time of functions
    def time_attempt_0():
        wait_for_AWG(AWG, 0)
        return

    def time_attempt_1():
        wait_for_AWG(AWG, 1)
        return

    def time_attempt_2():
        wait_for_AWG(AWG, 2)
        return

    def time_attempt_3():
        wait_for_AWG(AWG, 3)
        return

    def time_attempt_4():
        wait_for_AWG(AWG, 4)
        return

    # use t as ouput for showing running time of wait_for_AWG in form of:
    # t = timeit.timeit(time_attempt_X, number=1)
    # optionally output with position enabling connection between output and code-function:
    # print("Laufzeit von time_attempt in milli Sec: " + str(t*1e3) + " at position XY")
    t = 0
    error_nr = 0    # Counter for number of errors

    # check for correct minimum duration of operating by using time_attempt_1
    # check for correct work of "OPC" with use of time_attempt_2
    # check for correct work of "WAI" with use of time_attempt_3
    # check for correct work of "Busy" with use of time_attempt_4
    # old: wait 10 sec with time_attempt_0

    # initialization of signal to use:
    f_rep = 900e3
    f_BB = 5e6
    Vpp = 0.3
    sample_rate_AWG_max = 2e8
    signal = generate_BBsignal(f_rep=f_rep, f_BB=f_BB, Vpp=Vpp, sample_rate_AWG_max=sample_rate_AWG_max,
                                   verbosity=0)

    # Implementation copy from write_to_AWG.write
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

    #Reset Instrument
    AWG.write("*RST")
    error = AWG.query("SYSTem:ERRor?")# reads and deletes one error - NEW
    while error.find('0') != -1:       # will this work, format of error should be string
        error_nr = error_nr +1
        print("Error Number " + str(error_nr) + " at beginning of code with error: " + str(error))
        error = AWG.query("SYSTem:ERRor?")

    AWG.write("SOURce1:FUNCtion:ARBitrary:FILTer OFF")
    AWG.write("SOURce2:FUNCtion:ARBitrary:FILTer OFF")

    # time analysis Position 1
    t = timeit.timeit(time_attempt_1, number=1)
    print("Laufzeit von time_attempt_1 in milli Sec: " + str(t*1e3) + " at Position 1")
    t = 0

    AWG.write("DATA:VOLatile:CLEar")
    myrange = max(abs(max(signal.in_V)), abs(min(signal.in_V)))
    # Data Conversion from V to DAC levels
    data_conv = np.round(signal.in_V * 32766 / myrange);
    data_conv = ",".join(str(e) for e in data_conv)
    AWG.write("SOURce1:DATA:ARBitrary:DAC myarb ," + data_conv)

    # time analysis Position 2
    t = timeit.timeit(time_attempt_3, number=1)
    print("Laufzeit von time_attempt_3 in milli Sec: " + str(t * 1e3) + " at Position 2")
    t = 0

    AWG.write("SOURce1:FUNCtion:ARBitrary 'myarb'")

    # time analysis Position 3
    t = timeit.timeit(time_attempt_3, number=1)
    print("Laufzeit von time_attempt_3 in milli Sec: " + str(t * 1e3) + " at Position 3")
    t = 0

    AWG.write("SOURce1:FUNCtion ARB")  # USER
    AWG.write("DISPlay:FOCus CH1")
    AWG.write("DISPlay:UNIT:ARBRate SRATe") # because frequency is given, sample rate is of more interest
    #AWG.write("SOURce1:FUNCtion:ARBitrary:SRATe " + str(sample_rate_AWG_max))
    AWG.write("SOURce1:FUNCtion:ARBitrary:FREQ " + str(f_rep))

    # time analysis Position 4
    t = timeit.timeit(time_attempt_0, number=1)
    print("Laufzeit von time_attempt_0 in milli Sec: " + str(t * 1e3) + " at Position 4")
    t = 0

    AWG.write("SOURce2:DATA:ARBitrary:DAC myarb ," + data_conv)

    # time analysis Position 5
    t = timeit.timeit(time_attempt_2, number=1)
    print("Laufzeit von time_attempt_2 in milli Sec: " + str(t * 1e3) + " at Position 5")
    t = 0

    error = AWG.query("SYSTem:ERRor?")# reads and deletes one erro - NEW
    while error.find('0') != -1:       # will this work, format of error should be string
        error_nr = error_nr +1
        print("Error Number " + str(error_nr) + " after writing signal with error: " + str(error))
        error = AWG.query("SYSTem:ERRor?")

    AWG.write("SOURce2:FUNCtion:ARBitrary 'myarb'")

    # time analysis Position 6
    t = timeit.timeit(time_attempt_2, number=1)
    print("Laufzeit von time_attempt_2 in milli Sec: " + str(t * 1e3) + " at Position 6")
    t = 0

    AWG.write("SOURce2:FUNCtion ARB")  # USER
    AWG.write("DISPlay:FOCus CH2")
    AWG.write("DISPlay:UNIT:ARBRate FREQuency")
    AWG.write("SOURce2:FUNCtion:ARBitrary:FREQ " + str(f_rep))
    # AWG.write("SOURce2:FUNCtion:ARBitrary:SRATe " + str(sample_rate_AWG_max))
    AWG.write("FUNC:ARB:SYNC")
    AWG.write("SOURce1:VOLTage " + str(Vpp))
    AWG.write("SOURce2:VOLTage " + str(Vpp))

    # time analysis Position 3
    t = timeit.timeit(time_attempt_3, number=1)
    print("Laufzeit von time_attempt_3 in milli Sec: " + str(t * 1e3) + " at Position 3")
    t = 0

    AWG.write("OUTPut1 OFF")
    AWG.write("OUTPut2 OFF")
    AWG.write("DISPlay:FOCus CH1")

    error = AWG.query("SYSTem:ERRor?")# reads and deletes one erro - NEW
    while error.find('0') != -1:       # will this work, format of error should be string
        error_nr = error_nr +1
        print("Error Number " + str(error_nr) + " at end of code with error: " + str(error))
        error = AWG.query("SYSTem:ERRor?")

    return


def check_DSO():
    """
    # !!! apply a SIGNAL with Frequency fmax = 900 kHz and Vpp = 0.3 V to the DSO channel 1 before starting!

    checks whether the DSO is connected correctly before starting the program to avoid program mistakes in functionality running.
    Especially enables to check code to communicate with the DSO like the run-time optimization.
    This implementation only uses channel 1 to check which therefor needs to be connected to a signal.

    check for correct work of "WAI" with use of time_attempt_1
    check for correct work of "OPC" with use of time_attempt_2
    check for correct work of "Busy" with use of time_attempt_3
    old: wait 5 sec with time_attempt_0

    use t as ouput for showing running time in form of:
    t = timeit.timeit(time_attempt_X, number=1)
    optionally output with position enabling connection between output and code-function:
    print("Laufzeit von time_attempt in milli Sec: " + str(t*1e3) + " at position XY")
    reset t = 0

    :return: nothing
    """

    # Define functions to use time-analysis by timeit.timeit
    # TODO: find clever solution instead of following, ugly implementation for measuring run-time
    def time_attempt_0():
        wait_for_DSO(DSO, 0)
        return

    def time_attempt_1():
        wait_for_DSO(DSO, 1)
        return

    def time_attempt_2():
        wait_for_DSO(DSO, 2)
        return

    def time_attempt_3():
        wait_for_DSO(DSO, 3)
        return

    t = 0


    # initialization
    sample_rate_DSO = 9999e5
    fmax = 900e3
    vpp = 0.3
    # !!! apply a SIGNAL with Frequency fmax and Vpp to the DSO channel 1 before starting!

    # copy of read_from_DSO.read

    dso_ip = 'TCPIP::169.254.225.181::gpib0,1::INSTR'
    DSO = visa.ResourceManager().get_instrument(dso_ip)

    periodTime = 1 / fmax
    horizontalScalePerDiv = 1.5 * periodTime / 10 # try with 1.5 periods on screen

    possibleRecordLength = [500, 2500, 5000, 10e3, 25e3, 50e3, 100e3, 250e3, 500e3]
    possibleRecordLength = np.array(possibleRecordLength)

    ##WRITE DSO
    DSO.write("*RST")  # Restores the state of the instrument from a copy of
    # the settings stored in memory
    DSO.write("ACQUIRE:STATE OFF")  # This command stops acquisitions
    DSO.write("SELECT:CH1 ON")  # Turns the channel 1 waveform display on, and
    # selects channel 1.

    DSO.write("TRIGger:A:EDGE:SOUrce CH1")  # This command sets or queries the
    # source for the A edge trigger.
    DSO.write("TRIGger:A:EDGE:SLOpe FALL")  # This command sets or queries the
    # slope for the A edge trigger.

    DSO.write("HORizontal:MAIn:SCAle " + str(horizontalScalePerDiv))  # Sets the
    # time per division for the time base
    # Here 1,5 periods are on screen. Necessary since Osci has only discrete
    # values for horizontal scale and it needs to be ensured that at least
    # one full period is in the screen
    horizontalScalePerDiv = DSO.query("HORizontal:MAIn:SCAle?")
    horizontalScalePerDiv = [float(s) for s
                             in horizontalScalePerDiv.split(',')]
    horizontalScalePerDiv = horizontalScalePerDiv[0]
    recordLength = horizontalScalePerDiv * 10 * sample_rate_DSO
    ind = np.argmin(np.abs(recordLength - possibleRecordLength))
    if possibleRecordLength[ind] < recordLength and \
            (ind + 1) < possibleRecordLength.size:
        recordLength = possibleRecordLength[ind + 1]
    else:
        recordLength = possibleRecordLength[ind]

    DSO.write("HORIZONTAL:RECOrdlength " + str(recordLength))  # 1e5
    # MN: Meine Vermutung: Skalierung pro Division.
    # MN: Eigentlich sind 8 Divisionen vorhaden; Vpp wird durch 6 geteilt -> Sicherheitsabstand
    DSO.write("CH1:SCAle " + str(vpp / 6))  # Sets the vertical scale
    DSO.write("MATH1:SCAle " + str(vpp / 6))  # Sets the vertical scale

    DSO.write("CH1:POSition 0")  # Sets the horizontal scale
    DSO.write("CH1:TERmination 1.0E+6")  # Sets the termination of the channel
    DSO.write("CH2:TERmination 1.0E+6")  # Sets the termination of the channel
    DSO.write("CH3:TERmination 1.0E+6")  # Sets the termination of the channel
    DSO.write("CH4:TERmination 1.0E+6")  # Sets the termination of the channel
    DSO.write("CH1:COUPling DC")  # Sets the coupling of channel 1 to AC
    # Coupling to AC since the input signal has no DC component.
    # No DC expected at the output. Use AC coupling to reduce influence
    # from outside.
    DSO.write("DATa:ENCdg ASCIi")  # This command sets the format of outgoing
    # waveform data to ASCII
    DSO.write("ACQUIRE:MODE SAMPLE")  # This command sets the acquisition mode
    # of the instrument to sample mode
    DSO.write("ACQUIRE:STOPAFTER SEQUENCE")  # Specifies that the next
    # acquisition will be a
    # single-sequence acquisition.
    DSO.write("HORizontal:MAIn:SAMPLERate " + str(sample_rate_DSO))  # Sets the
    # sample rate of the device.
    # Here: 10 times maximum expected
    # frequency to reduce aliasing
    DSO.write("ACQUIRE:STATE ON")  # This command starts acquisitions
    DSO.write("DATa:STARt 1")  # This command sets the starting data point
    # for waveform transfer. This command allows for the
    # transfer of partial waveforms to and from the instrument.
    DSO.write("DATa:STOP " + DSO.query("HORIZONTAL:RECOrdlength?"))  # Sets the
    # last data point that will be transferred when using the CURVe? query

    # time analysis Position 1
    t = timeit.timeit(time_attempt_0, number=1)
    print("Laufzeit von time_attempt_0 in milli Sec: " + str(t * 1e3) + " at Position 1")
    t = 0

    dataUin = DSO.query("CURVe?")
    #DSO.write("DATa:SOUrce MATH3")  # This command sets the location of
    # waveform data that is transferred from the
    # instrument by the CURVe? Query
    DSO.write("DATa:ENCdg ASCIi")  # This command sets the format of outgoing
    # waveform data to ASCII
    DSO.write("DATa:STARt 1")  # This command sets the starting data point
    # for wavefosrm transfer. This command allows for the
    # transfer of partial waveforms to and from the instrument.
    DSO.write("DATa:STOP " + DSO.query("HORIZONTAL:RECOrdlength?"))  # Sets the
    # last data point that will be transferred when using the CURVe? query

    # time analysis Position 2
    t = timeit.timeit(time_attempt_3, number=1)
    print("Laufzeit von time_attempt_3 in milli Sec: " + str(t * 1e3) + " at Position 2")
    t = 0

    # end copy from read_from_DSO.read


def wait_for_AWG(AWG, attempt=0):
    """

    :param AWG: the Signal Generator to wait for, - designed by visa resourcemanager open (here: just Keysight)
    :param attempt: choice of which wait-routine to run
    :return: nothing
    """

    if attempt == 1:
        time.sleep(1.3)  # simple to reduce time to wait
        # -> see data sheet: maximum time needed to write is given by 1.25 sec
    elif attempt == 2:
        AWG.query("*OPC?")  # new attempt 1 to reduce time to wait
        # -> does not proceed until *OPC? is set to 1 by internal queue.
        # so, finishing this line in the program will last until the device is ready
        # In case this is not working, try AWG.write("*OPC?") instead, just as a guess
        # can used as a boolean variable, finished = AWG.query("*OPC?"), if necessary for a loop
    elif attempt == 3:
        AWG.write("*WAI")  # new attempt 2 to reduce time to wait -> AWG will wait till commands above are finished.
        # python will go on and write the commands in the input buffer
        # they will be executed after WAI has finished
        # new attempt 2 and another not named attempt are possible, but 1 is faster and more stable
    elif attempt == 4:
        busy = 1 # initialize
        busy = AWG.write("BUSY?")  # new attempt to reduce time to wait -> runs until OPC? is set to 1
        # try additionally:
        # busy = AWG.read() # comnined with write-command above should be same as query
        print("busy:")
        print(busy)
        print("busy ready")
        while busy == '1':  # loop until not busy any more
            time.sleep(0.01)  # just to pose less requests to DSO, 10 msec waiting time -> not necessary
            busy = AWG.query("BUSY?")
            print(busy)  # just to have a control option -> not necessary, it an attempt work
    else:
        time.sleep(10)  # enough time to finish every Process -> original implementation
    return

def wait_for_DSO(DSO, attempt=0):
    """

    :param DSO: the DSO to wait for - designed by visa resourcemanager open (here: just DSO Tektronix)
    :param attempt: choice of which wait-routine to run
    :return: nothing
    """
    if attempt == 1:
        DSO.write("*WAI")   #new attempt 1 to reduce time to wait -> DSO will wait till commands above are finished.
                            # python will go on and write the commands in the input buffer
                            # they will be executed after WAI has finished


    elif attempt == 2:
        DSO.query("*OPC?")  #new attempt 2 to reduce time to wait -> does not proceed until *OPC? is set to 1 by internal queue.
                        # so, finishing this line in the program will last until the device is ready
                        # In case this is not working, try DSO.write("*OPC?") instead, just as a guess
                        # can used as a boolean variable, finished = DSO.query("*OPC?"), if necessary for a loop
    elif attempt == 3:
        busy = DSO.query("BUSY?")          #new attempt 3 to reduce time to wait -> runs until OPC? is set to 1
        while busy=="1":                        #loop until not busy any more
               time.sleep(0.01)         #just to pose less requests to DSO, 10 msec waiting time -> not necessary
               busy = DSO.query("BUSY?")
               print(busy)                 #just to have a control option -> not necessary, it an attempt work
                                        # In case this is not working, try DSO.write("BUSY") instead, just as a guess
    else :
        time.sleep(5)  # enough time to finish every Process

        # new attempt 1 and another not named attempt are possible, but 2 and 3 are faster and more stable following the description

    return





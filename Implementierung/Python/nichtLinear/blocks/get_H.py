# -*- coding: utf-8 -*-
"""
Created on Tue Feb 21 13:10:28 2017
updated version 27.10.17

@author: Armin Galetzka, Denys Bast
Measures and calculates the transfer function of a two port.
Requirements:
    - AWG with two output ports
    - Channel 1 at oscilloscope is output signal of AWG
    - Modus FALSE: Channnel 3 and 4 are connected to the output of the two port and 
      the quantity of interest is calculated by CH3-CH4
    - Modus TRUE: Channnel 3 is connected to the output 


Input:  fmax          ------  max frequency of interest
        Vpp           ------  Output peak-peak voltage of AWG
        bits          ------  
        writeAWG      ------  True: write input signal on awg
        showPlots     ------  If True plots are shown and saved as .pdf
        createCSV     ------  If True a CSV file for each quantity of interest
                              is created
        formatOutput  ------  0=dB, 1=linear, 2=both
        modus         ------  False CH3-CH4, True CH3, 1Channel vs 2Channel
"""


def get_H(fmax, Vpp, bits=10, writeAWG=True, showPlots=0, createCSV=1, \
          formatOutput=1):
    import visa
    from helpers import MLBS
    import time
    import matplotlib.pyplot as plt
    import numpy as np
    from helpers import FFT, write_to_AWG, read_from_DSO_resolution, read_from_DSO
    import csv
    import os

    from settings import use_mock_system, mock_system, last_directory_used, get_H_data_path_real_system, get_H_data_path_mock
    import  settings

    # Create folder for results
    if use_mock_system:
        get_H_data_path = get_H_data_path_mock
    else :
        get_H_data_path = get_H_data_path_real_system


    directory = get_H_data_path + time.strftime("%d.%m.%Y_%H_%M_%S") + '/'
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.exists(directory + "/Plots"):
        os.makedirs(directory + "/Plots")
    if not os.path.exists(directory + "/csv"):
        os.makedirs(directory + "/csv")

    ### save directory name

    settings.set_last_directory_used(directory + "csv/")

    # Parameter
    awg_volt = Vpp
    samplerateAWG = 2.5 * fmax
    samplerateOszi = 100 * samplerateAWG
    fPlot = fmax
    possibleRecordLength = [500, 2500, 5000, 10e3, 25e3, 50e3, 100e3, 250e3, 500e3]
    possibleRecordLength = np.array(possibleRecordLength)
    linewidthPlot = 1

    font = {'family': 'normal',
            'weight': 'normal',
            'size': 12}

    plt.rc('font', **font)

    [signal, seed] = MLBS.get(bits)
    Tns = 0.4 / fmax
    periodTime = signal.size * Tns
    horizontalScalePerDiv = 1.5 * periodTime / 10  # At least one period needs to be
    # shown on the DSO

    ########################
    original_signal = signal
    ########################

    if use_mock_system :
        mock_system.write_to_AWG(signal=signal, awg_Vpp=awg_volt, samplerateAWG=samplerateAWG)

        time, dataUin, dataUout = mock_system.read_from_DSO_resolution(samplerateOszi=samplerateOszi,
                                                                        vpp_ch1=awg_volt, fmax=fmax,
                                                                        signal=signal)
    else :

        # am Desktop PC
        # dso_ip = rs[1]
        # am Gruppenlaptop BTNBG006
        dso_ip = 'TCPIP::169.254.225.181::gpib0,1::INSTR'
        DSO = visa.ResourceManager().get_instrument(dso_ip)

        write_to_AWG.write_to_AWG(signal=signal, awg_Vpp=awg_volt, samplerateAWG=samplerateAWG)

        time, dataUin, dataUout = read_from_DSO_resolution.read_from_DSO_resolution(samplerateOszi=samplerateOszi,
                                                                                    vpp_ch1=awg_volt, fmax=fmax,
                                                                                    signal=signal, measure_H = True)






    # Compute FFT of signals in time domain
    [frq, UinAmpl, PhaseUin, Uin] = FFT.get(dataUin, 1 / (time[-1] - time[-2]));
    [frq, UoutAmpl, PhaseUout, Uout] = FFT.get(dataUout, \
                                               1 / (time[-1] - time[-2]));

    # Reduce frequency domain signal to maximum frequency fPlot
    ind = np.argmin(abs(frq - fPlot))
    frq = frq[0:ind]
    UinAmpl = UinAmpl[0:ind]
    UoutAmpl = UoutAmpl[0:ind]
    Uin = Uin[0:ind]
    Uout = Uout[0:ind]
    PhaseUout = PhaseUout[0:ind]
    PhaseUin = PhaseUin[0:ind]

    # Compute transer function
    H = UoutAmpl / UinAmpl
    Phase = np.angle(Uout / Uin)
    # PhaseH = PhaseUout-PhaseUin
    # No DC component!
    H = H[1:]
    UinAmpl = UinAmpl[1:]
    UoutAmpl = UoutAmpl[1:]
    frq = frq[1:]
    Uin = Uin[1:]
    Uout = Uout[1:]
    Phase = Phase[1:]

    # Phase bereinigen, Phasensprung korrigieren

    PhaseH = np.asarray([float(i) for i in Phase])
    PhaseVGL = [float(i) for i in Phase]

    # Phase bereinigen, Phasensprung korrigieren

    for ind in range(0, (len(Phase) - 1)):
        if PhaseVGL[ind] * PhaseVGL[ind + 1] < 0:
            if PhaseVGL[ind] > np.pi / 2 and PhaseVGL[ind + 1] < -np.pi / 2:
                PhaseH[ind + 1:] = PhaseH[ind + 1:] + 2 * np.pi
            elif PhaseVGL[ind] < -np.pi / 2 and PhaseVGL[ind + 1] > np.pi / 2:
                PhaseH[ind + 1:] = PhaseH[ind + 1:] - 2 * np.pi

    ##################################################
    ############## Plots #############################
    ##################################################

    if showPlots:

        f = 0
        fig = plt.figure(f + 1)
        f += 1
        plt.plot(time * 1e6, dataUin, linewidth=linewidthPlot)
        plt.ylabel(r'$U_{\mathrm{in}}(t)$')
        plt.xlabel(r'$t$ in $\mu$s')
        plt.grid(True)
        fig.savefig(directory + "/Plots/Uin_time.pdf", bbox_inches='tight')
        plt.show()

        fig = plt.figure(f + 1)
        f += 1
        plt.plot(time * 1e6, dataUout, linewidth=linewidthPlot)
        plt.ylabel(r'$U_{\mathrm{out}}(t)$')
        plt.xlabel(r'$t$ in $\mu$s')
        plt.grid(True)
        fig.savefig(directory + "/Plots/Uout_time.pdf", bbox_inches='tight')
        plt.show()

        fig = plt.figure(f + 1)
        f += 1
        plt.plot(frq / 1e6, PhaseH, linewidth=linewidthPlot)
        plt.ylabel(r'arg($H(\omega)$)')
        plt.xlabel(r'$f$ in MHz')
        plt.grid(True)
        fig.savefig(directory + "/Plots/PhaseH.pdf", bbox_inches='tight')
        plt.show()

        if (formatOutput == 0) or (formatOutput == 2):
            fig = plt.figure(f + 1)
            f += 1
            plt.plot(frq / 1e6, 20 * np.log10(UinAmpl), linewidth=linewidthPlot)
            plt.grid(True)
            plt.ylabel(r'$|U_{\mathrm{in}}(f)|$ in dB')
            plt.xlabel(r'$f$ in MHz')
            fig.savefig(directory + "/Plots/UinAmpl_frq_dB.pdf", \
                        bbox_inches='tight')
            plt.show()

            fig = plt.figure(f + 1)
            f += 1
            plt.plot(frq / 1e6, 20 * np.log10(UoutAmpl), linewidth=linewidthPlot)
            plt.grid(True)
            plt.ylabel(r'$|U_{\mathrm{out}}(f)|$ in dB')
            plt.xlabel(r'$f$ in MHz')
            fig.savefig(directory + "/Plots/UoutAmpl_frq_dB.pdf", \
                        bbox_inches='tight')
            plt.show()

            fig = plt.figure(f + 1)
            f += 1
            plt.plot(frq / 1e6, 20 * np.log10(H), linewidth=linewidthPlot)
            plt.grid(True)
            plt.ylabel(r'$|H(f)|$ in dB')
            plt.xlabel(r'$f$ in MHz')
            fig.savefig(directory + "/Plots/H_dB.pdf", bbox_inches='tight')
            plt.show()

        if (formatOutput == 1 or formatOutput == 2):
            fig = plt.figure(f + 1)
            f += 1
            plt.plot(frq / 1e6, UinAmpl, linewidth=linewidthPlot)
            plt.grid(True)
            plt.ylabel(r'$|U_{\mathrm{in}}(f)|$')
            plt.xlabel(r'$f$ in MHz')
            fig.savefig(directory + "/Plots/UinAmpl_frq_linear.pdf", \
                        bbox_inches='tight')
            plt.show()

            fig = plt.figure(f + 1)
            f += 1
            plt.plot(frq / 1e6, UoutAmpl, linewidth=linewidthPlot)
            plt.grid(True)
            plt.ylabel(r'$|U_{\mathrm{out}}(f)|$')
            plt.xlabel(r'$f$ in MHz')
            fig.savefig(directory + "/Plots/UoutAmpl_frq_linear.pdf", \
                        bbox_inches='tight')
            plt.show()

            fig = plt.figure(f + 1)
            f += 1
            plt.plot(frq / 1e6, H, linewidth=linewidthPlot)
            plt.grid(True)
            plt.ylabel(r'$|H(f)|$')
            plt.xlabel(r'$f$ in MHz')
            fig.savefig(directory + "/Plots/H_linear.pdf", bbox_inches='tight')
            plt.show()
    ##################################################
    ############## Create CSV ########################
    ##################################################

    if createCSV:

        with open(directory + '/csv/UinTime.csv', 'w', newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=';',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for i in range(0, dataUin.size):
                writer.writerow([str(time[i]), str(dataUin[i])])

        with open(directory + '/csv/UoutTime.csv', 'w', newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=';',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for i in range(0, dataUout.size):
                writer.writerow([str(time[i]), str(dataUout[i])])

        with open(directory + '/csv/PhaseH.csv', 'w', newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=';',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for i in range(0, PhaseH.size):
                writer.writerow([str(frq[i]), str(PhaseH[i])])

        if (formatOutput == 1) or (formatOutput == 2):

            with open(directory + '/csv/UinAmplFrq_linear.csv', 'w', \
                      newline="") as csvfile:
                writer = csv.writer(csvfile, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for i in range(0, UinAmpl.size):
                    writer.writerow([str(frq[i]), str(UinAmpl[i])])

            with open(directory + '/csv/UoutAmplFrq_linear.csv', 'w', \
                      newline="") as csvfile:
                writer = csv.writer(csvfile, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for i in range(0, UoutAmpl.size):
                    writer.writerow([str(frq[i]), str(UoutAmpl[i])])

            with open(directory + '/csv/HAmpl_linear.csv', 'w', \
                      newline="") as csvfile:
                writer = csv.writer(csvfile, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for i in range(0, H.size):
                    writer.writerow([str(frq[i]), str(H[i])])

        if (formatOutput == 0 or formatOutput == 2):

            with open(directory + '/csv/UinAmplFrq_dB.csv', 'w', \
                      newline="") as csvfile:
                writer = csv.writer(csvfile, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for i in range(0, UinAmpl.size):
                    writer.writerow([str(frq[i]),
                                     str(20 * np.log10(UinAmpl[i]))])

            with open(directory + '/csv/UoutAmplFrq_dB.csv', 'w', \
                      newline="") as csvfile:
                writer = csv.writer(csvfile, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for i in range(0, UoutAmpl.size):
                    writer.writerow([str(frq[i]),
                                     str(20 * np.log10(UoutAmpl[i]))])

            with open(directory + '/csv/HAmpl_dB.csv', 'w', \
                      newline="") as csvfile:
                writer = csv.writer(csvfile, delimiter=';',
                                    quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for i in range(0, H.size):
                    writer.writerow([str(frq[i]), str(20 * np.log10(H[i]))])

        with open(directory + '/csv/UinFrq.csv', 'w', newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=';',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for i in range(0, Uin.size):
                writer.writerow([str(frq[i]), str(Uin[i])])

        with open(directory + '/csv/UoutFrq.csv', 'w', newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=';',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for i in range(0, Uout.size):
                writer.writerow([str(frq[i]), str(Uout[i])])

        PhaseUin_save = PhaseUin[1:]
        PhaseUout_save = PhaseUout[1:]

        with open(directory + '/csv/UinPhase.csv', 'w', newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=';',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for i in range(0, PhaseUin_save.size):
                writer.writerow([str(frq[i]), str(PhaseUin_save[i])])

        with open(directory + '/csv/UoutPhase.csv', 'w', newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=';',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for i in range(0, PhaseUout_save.size):
                writer.writerow([str(frq[i]), str(PhaseUout_save[i])])

        with open(directory + '/csv/OriginalSignal.csv', 'w', newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=';',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            for i in range(0, original_signal.size):
                writer.writerow([str(original_signal[i])])

        with open(directory + '/csv/Samplerates.csv', 'w', newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=';',
                                quotechar='|', quoting=csv.QUOTE_MINIMAL)
            writer.writerow([ 'samplerateOszi' , str(samplerateOszi)])
            writer.writerow([ 'samplerateAWG', str(samplerateAWG)])

    return (frq, H, PhaseH)



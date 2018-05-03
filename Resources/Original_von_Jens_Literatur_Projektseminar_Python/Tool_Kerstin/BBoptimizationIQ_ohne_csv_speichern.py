#!/usr/bin/env python
# BB optimization software
# GSI-PBRF (K. Gross using the Group DDS calibration software of D. Lens), 2016
# version 1.1, 2017
# import argparse, subprocess
from __future__ import print_function
import sys
import time
import matplotlib.pyplot as plt
import colorama
import visa
import numpy as np
import csv
import struct

# # Initialization of colored text output:
colorama.init()

print(colorama.Back.GREEN + colorama.Style.BRIGHT + "BBoptimization: Start." + colorama.Style.NORMAL + colorama.Back.RESET)

# Default Parameters:
rev_freq = 9E5
bbp_freq = 50E5
max_iter = 1
perioden = 8
aufloes = 12500
act_var = 'AWG' # alternativen 'DSO' 'AWG' (Eingang auslesen?)
sys_var = 'I' # 'I' Ideal transformer, 'W' White noise
fdpt = 88 # Anzahl an Fourierkoeffizienten
filename_output = 'Messung_000_'

M = [4E-4,2E-4,1E-4,4E-5,2E-5,1E-5,4E-6,2E-6,1E-6,4E-7,2E-7,8E-8,4E-8,2E-8,1E-8,4E-9,2E-9,1.25E-9,1E-9]
myM = [i for i in M if i>=perioden/rev_freq/10-1E-21] # zeitachse in s/div
myM = min(myM)
myT = int(aufloes/myM/10*(perioden/rev_freq))
if sys_var == 'T':
	InputFile = open(filename_input)
	InputReader = csv.reader(InputFile)
	InputData = list(InputReader)
	InputData = [i for i in InputData if i != ['','','']]
	InputMatrix = np.array(InputData)
	InputMatrix = InputMatrix.astype(np.float)
	ueftk_f = InputMatrix.T[0]
	ueftk_a = InputMatrix.T[1]
	ueftk_b = InputMatrix.T[2]
	InputFile.close()
	fdpt = max(ueftk_f)//rev_freq

time.sleep(1)
sys_f = np.linspace(rev_freq,(fdpt*rev_freq),num=fdpt,endpoint=True,retstep=False)
output_c = np.zeros(fdpt)
output_s = (np.sinc((bbp_freq-sys_f)/bbp_freq)-np.sinc((bbp_freq+sys_f)/bbp_freq))

ist_t = np.linspace(0,(perioden/sys_f[0]),num=myT,endpoint=False,retstep=False)
print(colorama.Back.YELLOW + colorama.Style.BRIGHT + "BBoptimization: Building reference signal." + colorama.Style.NORMAL + colorama.Back.RESET, end="")
output_y = np.array([np.array([output_c[i]*np.cos(2*np.pi*sys_f[i]*t)+output_s[i]*np.sin(2*np.pi*sys_f[i]*t) for i in range(0,len(sys_f))]).sum() for t in ist_t])
print(colorama.Back.YELLOW + colorama.Style.BRIGHT + " Done." + colorama.Style.NORMAL + colorama.Back.RESET)
nex = 8*int(3E8/rev_freq/8) # myT/perioden
input_t = np.linspace(0,(1/sys_f[0]),num=nex,endpoint=True,retstep=False)

time.sleep(1)
if sys_var == 'I':
	sys_a = np.ones(fdpt)
	sys_b = np.zeros(fdpt)

time.sleep(1)
if sys_var == 'W':
	sys_a = output_c # ToDo
	sys_b = output_s # ToDo

time.sleep(1)
sys_2=(sys_a**(2) + sys_b**(2))**(-1.0)

# speichern
time.sleep(1)

# Connect to Instruments
def rein (x):
	time.sleep(1)
	TE.write(x + "{:04X}".format(sum(map(ord, x))) + chr(0))
	
def raus (y):
	time.sleep(1)
	x=TE.read()
	if x != unicode('\x00')+unicode(y)+unicode('\x0A'):
		print('Code line ' + str(sys._getframe(1).f_lineno) + ': ', end="")
		print(x)
		print([hex(ord(c)) for c in x])
	time.sleep(1)

print(colorama.Back.YELLOW + colorama.Style.BRIGHT + "BBoptimization: Connecting to instruments." + colorama.Style.NORMAL + colorama.Back.RESET, end="")
rm = visa.ResourceManager()
rs = rm.list_resources()
time.sleep(1)
TE = rm.open_resource(rs[-1], baud_rate = 115200, write_termination='')
rein("*Idn?")
print(TE.read()[:-1])
rein("*RST")
raus('0')
rein("*CLS")
raus('0')

dso_ip = rs[0]
DSO = visa.ResourceManager().get_instrument(dso_ip)
DSO.write("*RST")
DSO.write("*CLS")
print(colorama.Back.YELLOW + colorama.Style.BRIGHT + " Done." + colorama.Style.NORMAL + colorama.Back.RESET)
## Schleife
time.sleep(5)

for cnt in range(0,max_iter):
	awg_volt = 0.1
	myA =  0.3*awg_volt
	print("BBoptimization: Pass " + str(cnt+1) + " of " + str(max_iter) + ".")
	input_c = sys_a*output_c + sys_b*output_s
	input_c[np.isnan(input_c)] = 0
	input_s = -sys_b*output_c + sys_a*output_s
	input_s[np.isnan(input_s)] = 0
	# Signals FD2TD
	input_y = np.array([np.array([input_c[i]*np.cos(2*np.pi*sys_f[i]*t)+input_s[i]*np.sin(2*np.pi*sys_f[i]*t) for i in range(0,len(sys_f))]).sum() for t in input_t])	
	input_y = input_y - input_y[0]
	time.sleep(1)
	myrange=max(abs(max(input_y)),abs(min(input_y)))*(1+0.5/2047)
	data_conv=np.round(input_y*2047/myrange)+2048;
	#str_u = ",".join(str(e) for e in data_conv)
	lst_u = data_conv.tolist()
	buf = struct.pack('%sh' % len(lst_u), *lst_u)
	checksum = int(sum((data_conv[g]-(data_conv[g]%(16*16)))/16/16+data_conv[g]%(16*16) for g in range(len(data_conv)))) 

	rein("*RST")
	raus('0')
	rein(":TRAC:DEL: ALL;:SYST:ERR?")
	raus('0;0,"No error"')
	rein(":TRAC:DEF 1," + str(nex) + ";:TRAC:SEL 1;:SYST:ERR?")
	raus('0;0,"No error"')
	rein("trace #")
	time.sleep(1)
	TE.write(str(len(str(2*nex))))
	TE.write(str(2*nex))
	time.sleep(1)
	raus('0')
	time.sleep(1)
	TE.write_raw(buf)
	TE.write("{:04X}".format(checksum))
	time.sleep(10)
	raus('000\r')
	time.sleep(1)
	rein(":INST:SEL 1;:APPLy:USER 1," + str(rev_freq*(nex-1)) + "," + str(awg_volt) + ",0.000E0;:SYST:ERR?")
	raus('0;0,"No error"')

	input_y = input_y/np.max(np.abs(input_y)*1.1)
	# Write to DSO for output
	DSO.write("*RST")
	DSO.write("SELECT:CH1 OFF")
	DSO.write("MATH1:DEFIne 'CH3-CH2'")#DSO.write("MATH1:DEFIne 'CH3-CH2'")
	DSO.write("CH4:TERmination 50.0E+0")
	DSO.write("SELECT:CH4 ON")
	DSO.write("CH4:SCAle 0.2")
	DSO.write("TRIGger:A:EDGE:SOUrce CH4")
	DSO.write("TRIGger:A:EDGE:SLOpe FALL")
	DSO.write("HORizontal:MAIn:SCAle " + str(myM))
	DSO.write("HORizontal:MAIn:POSition 0")
	DSO.write("HORizontal:RESOlution " + str(aufloes))
	DSO.write("MATH1:NUMAVg 1")
	DSO.write("SELECT:MATH1 ON")
	DSO.write("MATH1:VERTical:SCAle " + str(myA))
	DSO.write("MATH1:SCAle " + str(myA))
	DSO.write("CH2:SCAle " + str(myA/2))
	DSO.write("CH3:SCAle " + str(myA/2))
	DSO.write("DATa:SOUrce MATH1")
	DSO.write("DATa:ENCdg SRFBinary")
	DSO.write("DATa:STARt 1")
	DSO.write("DATa:STOP " + str(myT))

	time.sleep(5)
	DSO.write("ACQuire:STOPAfter SEQuence")
	DSO.write("MATH1:VERTical:SCAle " + str(myA))
	DSO.write("MATH1:SCAle " + str(myA))
	DSO.write("MATH1:POSition 0")
	DSO.write("CH2:SCAle " + str(myA/2))
	DSO.write("CH3:SCAle " + str(myA/2))
	print(colorama.Back.YELLOW + colorama.Style.BRIGHT + "BBoptimization: Reading DSO data." + colorama.Style.NORMAL + colorama.Back.RESET, end="")
	time.sleep(5)
	ist_y = DSO.query_binary_values('CURVe?', datatype='f', is_big_endian=True, container=np.array)
	print(colorama.Back.YELLOW + colorama.Style.BRIGHT + " Done." + colorama.Style.NORMAL + colorama.Back.RESET)
	DSO.write("HARDCopy STARt")
	time.sleep(1)
	ist_c = np.array([np.array([ist_y[i]*np.cos(2*np.pi*f*ist_t[i]) for i in range(0,len(ist_t))]).sum() for f in sys_f])/myT*2
	time.sleep(1)
	ist_s = np.array([np.array([ist_y[i]*np.sin(2*np.pi*f*ist_t[i]) for i in range(0,len(ist_t))]).sum() for f in sys_f])/myT*2
	time.sleep(5)

	# System FD
	sys_a = (input_c*ist_c+input_s*ist_s)*(ist_c**(2)+ist_s**(2))**(-1.0)
	sys_b = (input_c*ist_s-input_s*ist_c)*(ist_c**(2)+ist_s**(2))**(-1.0)
	# speichern
	
print(colorama.Back.GREEN + colorama.Style.BRIGHT + "BBoptimization: Done." + colorama.Style.NORMAL + colorama.Back.RESET)
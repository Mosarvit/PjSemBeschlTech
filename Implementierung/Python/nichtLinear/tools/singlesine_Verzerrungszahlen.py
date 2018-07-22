#!/usr/bin/python3
#@author: Mohamed Ghanmi
from __future__ import division

version_string = 'Rev. 0.0.4, 21.06.2018'
import tools.rftools_bcf
import pandas as pd
from pandas import read_csv
import numpy as np
import os, sys, glob, argparse, colorama, time
from math import ceil,floor
import matplotlib.pyplot as plt

from tools.singlesine_Signal import Einlesen


# Documentation data for Doxygen
## @package singlesine_SineRef.py
# Calculates the discrete Fourier transform of a sampled signal (ti, yi)
#
#
# \param[in] -h Help switch.
# \param[in] -i Name of input file.
# \param[in] -signal Name of the output file generated from singlesine_Signal.
# \param[in] -ref Name of the output file generated from singlesine_SineRef.
# \param[in] -frev Wiederholfrequenz.
# \param[in] -fBB Barier-Bucket-Frequenz.
# \param[in] -o Name of output file.
# \param[out] Integer number as error code (0: success, 1: general error, 10: error due to input parameters, 20: error while reading an input file, 21: input file has incorrect file format, 22: input file is empty, 30: error while writing the output file, 31: output file already exists)

def Verzerrungszahlen(dataPointsRef,dataPointsSignal,PulseOn,PointsPulse,PulseA,PulseP,frev,fBB,flag):
	"""
	Bestimmt verschiedene Guetemasse zwischen
	dem gemessenen Signal und einem Referenz-Einzelsinus

	Ausgabe: Quadratische Guete des Gesamtsignals, quadratische Guete des Pulses,Mittelwert des Pulses,
			 quadratische Guete zwischen den Pulsen
			 Alle Ausgabesignale sind auf die Anzahl der Abtastpunkte und die
			 Amplitude des Referenzsinus normiert

	Eingabe: Referenzsignal, Messsignal, PulseOn( nur inderhalb des Pulses 1)
			 Anzahl der Abtastpunkte innerhalb des Pulses, Amplitude, Phase
			 des Pulses, Umlauf-, Barrier-Bucket-Frequenz, name der Datei)

	Normieren der Signale auf dem Maximum des Referenzsignals
	"""
	result = {}
	flag = flag[:flag.index('.')]
	#print(flag)
	dataPointsSignalN = dataPointsSignal/max(dataPointsRef)
	dataPointsRefN = dataPointsRef/max(dataPointsRef)


	folder_exists  = os.path.isdir("Bilder")
	if not folder_exists:
		os.makedirs("Bilder")

	foldername = ""
	if "/" in flag:
		list = flag.split("/")
		foldername = flag.split("/")[0]
		N = len(list)
		if N > 2:
			for i in range(1, N - 1):
				foldername = foldername + '/' + list[i]

		flag = flag.split("/")[-1]

	nameBild ='Bilder/AbbildungTD_1P_' + str(flag)


	plt.plot(dataPointsSignal-np.mean(dataPointsSignal),'r',label = 'Signal')
	plt.plot(dataPointsRef,label = 'Referenz')
	plt.legend()
	#plt.savefig(nameBild)
	#plt.savefig(nameBild+'.pdf')
	#plt.show()
	plt.gcf().clear()
	#plt.show()

	#Variante 1 Mittelwert vom Puls abgezogen
	dataPointsSignalMWF1 = dataPointsSignalN - sum(dataPointsSignalN * (np.ones(len(dataPointsRefN))-PulseOn)) / sum((np.ones(len(dataPointsRef))-PulseOn))
	QGesamt1=1e2*np.sqrt(np.mean(power(dataPointsSignalMWF1-dataPointsRefN,2)))
	Qpulse1=1e2*np.sqrt(sum(power(dataPointsSignalMWF1-dataPointsRefN,2)*PulseOn)/PointsPulse)
	#CHECK sum dataPointsSignalN .........
	MWpulse1 = np.mean(dataPointsSignalMWF1)
	Qrest1=1e2*np.sqrt(sum(power(dataPointsSignalMWF1-dataPointsRefN,2)*(np.ones(len(dataPointsRefN))-PulseOn))/(len(dataPointsSignal)-PointsPulse))
	maxPulse1=1e2*max(abs(dataPointsSignalMWF1-dataPointsRefN)*PulseOn)
	maxRest1=1e2*max(abs(dataPointsSignalMWF1-dataPointsRefN)*(np.ones(len(dataPointsRef))-PulseOn))


	result['Amplitude'] = abs(PulseA)
	result['Phase'] = PulseP

	result['QGesamt1'] = QGesamt1
	result['Qpulse1'] = Qpulse1
	result['MWpulse1'] = MWpulse1
	result['Qrest1'] = Qrest1
	result['maxPulse1'] = maxPulse1
	result['maxRest1'] = maxRest1

	#Variante 2 Mittelwert des ganzen Signals
	dataPointsSignalMWF2 = dataPointsSignalN - np.mean(dataPointsSignalN)
	QGesamt2=1e2*np.sqrt(np.mean(power(dataPointsSignalMWF2-dataPointsRefN,2)))
	Qpulse2=1e2*np.sqrt(sum(power(dataPointsSignalMWF2-dataPointsRefN,2)*PulseOn)/PointsPulse)
	MWpulse2 = np.mean(dataPointsSignalMWF2)
	#CHECK MWpulse2
	Qrest2=1e2*np.sqrt(sum(power(dataPointsSignalMWF2-dataPointsRefN,2)*(np.ones(len(dataPointsRefN))-PulseOn))/(len(dataPointsSignal)-PointsPulse))
	maxPulse2=1e2*max(abs(dataPointsSignalMWF2-dataPointsRefN)*PulseOn)
	maxRest2=1e2*max(abs(dataPointsSignalMWF2-dataPointsRefN)*(np.ones(len(dataPointsRef))-PulseOn))

	result['QGesamt2'] = QGesamt2
	result['Qpulse2'] = Qpulse2
	result['MWpulse2'] = MWpulse2
	result['Qrest2'] = Qrest2
	result['maxPulse2'] = maxPulse2
	result['maxRest2'] = maxRest2

	#TODO INPUT FOLDER NAME
	# Code Kerstin
	#folder_name = 'csvDateien_K'
	if foldername != "":
		dateiName = foldername  +'/'+ flag +  '.csv'
	else:
		dateiName =  flag +  '.csv'

	SingleSine = read_csv(dateiName)

	t,messignal,t_Sample,HOffset,tShift = Einlesen(dateiName,foldername,SingleSine)
	t = np.array(t).astype(np.float)
	messignal *= 800

	# TD Plot mit Messdaten
	tphase = PulseP/360/frev
	tSSlogic = np.zeros(len(t))
	SSphase = np.zeros(len(t))


	for n in range (-1, int(ceil((t[-1]-t[0])*frev))):

		tSSlogic = matlab_max(tSSlogic,matlab_min(compare_array_2_number(array =t-t[0],number =tphase+n/frev,greaterOrLess = 0 ),compare_array_2_number(array =t-t[0],number =tphase+n/frev+1/fBB,greaterOrLess = 1 )))

		temp_SS1 = compare_array_2_number (array = t-t[0], number = tphase+n/frev , greaterOrLess = 0 )
		temp_SS2 = compare_array_2_number (array = t-t[0], number = tphase+n/frev+1/fBB , greaterOrLess = 1 )
		index_SS = matlab_min(temp_SS1,temp_SS2)
		i_SS = matlab_get_true_indexes(index_SS)
		value_SS = (matlab_get_subarray(t,i_SS)-t[0]-tphase-n/frev)*2*np.pi*fBB
		SSphase = matlab_update_array (SSphase,i_SS,value_SS)
	refsignal = PulseA*np.sin(SSphase)
	frevPerioden = ceil((t[-1]-t[0])*frev)
	tAbschluss = frevPerioden/frev


	i_ms = compare_array_2_number(array = t-t[0],number=tAbschluss,greaterOrLess=1)
	i_ms = matlab_get_true_indexes(i_ms)
	m = matlab_get_subarray(messignal,i_ms)
	mean = np.mean(m)
	if SingleSine.shape[1] == 2 :
		plt.plot(t,messignal - mean, label = 'Signal',linewidth=.1)
	else:
		plt.plot(t,messignal - mean, label = 'Signal',linewidth=.8)
	plt.plot(t,refsignal, 'r--',label =  'Referenz')
	nameBild= 'Bilder/AbbildungTD_'+str(flag)
	plt.legend()
	plt.savefig(nameBild)
	plt.savefig(nameBild+'.pdf')
	plt.gcf().clear()

	#Normieren der Signale auf dem Maximum des Referenzsignals
	messignalN = messignal/abs(max(refsignal))
	refsignalN = refsignal/abs(max(refsignal))

	#Calculating messignalMWF3
	not_tSSlogic = np.zeros(len(tSSlogic))
	for i in range(0,len(tSSlogic)):
		if tSSlogic[i] == 0:
			not_tSSlogic[i] = 1
	hv = matlab_get_subarray(messignalN,matlab_get_true_indexes(not_tSSlogic))
	hv = np.array (hv)
	messignalMWF3 = messignalN - np.mean (hv)
	diff = np.subtract(matlab_get_subarray(messignalMWF3,matlab_get_true_indexes(tSSlogic)) , matlab_get_subarray(refsignalN,matlab_get_true_indexes(tSSlogic)))
	QGesamt3 = 1e2*np.sqrt(np.mean(power(messignalMWF3-refsignalN,2)))
	Qpulse3=1e2*np.sqrt(np.mean(power(diff,2)))
	MWpulse3 = np.mean(messignalMWF3)
	Qrest3 = 1e2*np.sqrt(np.mean(power(matlab_get_subarray(messignalMWF3,matlab_get_true_indexes(not_tSSlogic)),2)))
	maxPulse3 = 1e2*max(abs(diff))
	maxRest3=1e2*max(abs(hv))

	#TODO VERY IMPORTANT CHECK MAXREST3

	result['QGesamt3'] = QGesamt3
	result['Qpulse3'] = Qpulse3
	result['MWpulse3'] = MWpulse3
	result['Qrest3'] = Qrest3
	result['maxPulse3'] = maxPulse3
	result['maxRest3'] = maxRest3

	messignalMWF4 = messignalN-np.mean(messignalN)
	QGesamt4 = 1e2*np.sqrt(np.mean(power(np.subtract(messignalMWF4,refsignalN),2)))
	diff = np.subtract(matlab_get_subarray(messignalMWF4,matlab_get_true_indexes(tSSlogic)),matlab_get_subarray(refsignalN,matlab_get_true_indexes(tSSlogic)))
	Qpulse4=1e2*np.sqrt(np.mean(power(diff,2)))
	MWpulse4 = np.mean(messignalMWF4)
	#TODO VERY IMPORTANT CHECK MWPULSE4
	hv = matlab_get_subarray(messignalMWF4,matlab_get_true_indexes(not_tSSlogic))
	hv = np.array (hv)
	Qrest4=1e2*np.sqrt(np.mean(power(hv,2)))
	maxPulse4=1e2*max(abs(diff))
	maxRest4=1e2*max(abs(hv))

	result['QGesamt4'] = QGesamt4
	result['Qpulse4'] = Qpulse4
	result['MWpulse4'] = MWpulse4
	result['Qrest4'] = Qrest4
	result['maxPulse4'] = maxPulse4
	result['maxRest4'] = maxRest4

	#Frequenzbereich(FD)
	t = matlab_get_subarray(t,matlab_get_true_indexes(compare_array_2_number(array =t-t[0],number=tAbschluss,greaterOrLess = 2))) - t[0]
	ym = matlab_get_subarray(messignal,np.arange(0,len(t)))
	ym[:] = [x / PulseA for x in ym]
	yr = matlab_get_subarray(refsignal,np.arange(0,len(t)))
	yr[:] = [x / PulseA for x in yr]
	fFD = np.arange(0,8e7,frev/frevPerioden) #Anzeige bis 80MzH
	#Initialisieren Amplitude Phase Messignal
	aFD = np.zeros(len(fFD))
	pFD = np.zeros(len(fFD))
	#Initialisieren Amplitude Phase Referenzsignal
	bFD = np.zeros(len(fFD))
	qFD = np.zeros(len(fFD))



#le reste n est pas verifie
	if t[-1] < tAbschluss:
		t = np.append(t,tAbschluss)
		t = t -tphase-1/2/fBB
		ym = np.append(ym,ym[0])
		yr = np.append(yr,yr[0])

	ym[-2] = ym[-2]*(1+(t[-1]-t[-2])/t[1])/2
	ym[-1] = ym[-1]*(t[-1]-t[-2])/t[1]/2
	ym[0]=ym[0]/2
	yr[-2]=yr[-2]*(1+(t[-1]-t[-2])/t[1])/2
	yr[-1]=yr[-1]*(t[-1]-t[-1])/t[1]/2
	yr[0]=yr[0]/2

	#plt.plot(t,ym,linewidth=.05)
	#plt.plot(t,yr,linewidth=3)
	#plt.show()
	for m in range(0,len(fFD)):
		#Messignal in FD
		temp_a = np.dot(np.cos(2*np.pi*fFD[m]*t),ym)
		temp_b = np.dot(np.sin(2*np.pi*fFD[m]*t),ym)
		aFD[m] = (temp_a**2+temp_b**2)**(1/2)/(len(t))/frev
		pFD[m] = np.arctan2(temp_b,temp_a)
		# Refsignal in FD
		temp_a = np.dot(np.cos(2*np.pi*fFD[m]*t),yr)
		temp_b = np.dot(np.sin(2*np.pi*fFD[m]*t),yr)
		bFD[m] = (temp_a**2+temp_b**2)**(1/2)/(len(t))/frev
		qFD[m] = np.arctan2(temp_b,temp_a)



	temp = np.arange(0,len(fFD),frevPerioden)
	temp = [ int(x) for x in temp]
	temp = matlab_get_subarray(fFD,temp) #fFD(1:frevPerioden:end)

	#FD Einzelsinus ideal
	temp1 = np.array(temp) + fBB
	temp1 *= -1
	temp1 /= fBB


	yFD = np.subtract(np.sinc(np.subtract(fBB,temp)/fBB),np.sinc(temp1))
	yFD /= 2
	yFD /= fBB

	plt.close()
	fig, (ax0, ax1) = plt.subplots(nrows=2, figsize=(16, 8))

	"""
	for ax in (ax0, ax1):
		ax.set_xscale('log')
	"""


	ax0.plot(fFD/1e6,bFD,'ro',color='red',label = 'ReferenzAP',markersize=3)#Alle punkte
	ax0.plot(fFD/1e6,aFD,'bo',label = 'SignalAP',markersize=3)

	ax0.plot(np.array(temp)/1e6,np.abs(yFD),'g>',label = 'Ideal',markersize=3)


	fFD_temp = temp
	bFD_temp = np.arange(0,len(bFD),frevPerioden)
	bFD_temp = [ int(x) for x in bFD_temp]
	bFD_temp = matlab_get_subarray(bFD,bFD_temp) #bFD(1:frevPerioden:end)

	ax0.plot(np.array(temp)/1e6,np.array(bFD_temp),'wo',markeredgecolor='red',label = 'Referenz',markersize=3) #jeder frevPerioden Punkt

	aFD_temp = np.arange(0,len(aFD),frevPerioden)
	aFD_temp = [ int(x) for x in aFD_temp]
	aFD_temp = matlab_get_subarray(aFD,aFD_temp) #bFD(1:frevPerioden:end)

	ax0.plot(np.array(temp)/1e6,np.array(aFD_temp),'bx',label = 'Signal',markersize=3)

	ax0.legend()

	#ax1
	temp = np.array(temp)/1e6

	qFD_temp = np.arange(0,len(qFD),frevPerioden)
	qFD_temp = [ int(x) for x in qFD_temp]
	qFD_temp = matlab_get_subarray(qFD,qFD_temp)

	pFD_temp = np.arange(0,len(pFD),frevPerioden)
	pFD_temp = [ int(x) for x in pFD_temp]
	pFD_temp = matlab_get_subarray(pFD,pFD_temp)

	ax1.plot(temp, np.arctan2(-yFD,0)/np.pi*180,'w>',markeredgecolor='green',label = 'Ideal',markersize=3)
	ax1.plot(temp, np.array(qFD_temp)/np.pi*180,'wo',markeredgecolor='red',label = 'Referenz',markersize=3)
	ax1.plot(temp, np.array(pFD_temp)/np.pi*180,'bx',label = 'Signal',markersize=3)
	ax1.legend()
	#plt.show()

	nameBild ='Bilder/AbbildungFBereich_' + str(flag)
	plt.savefig(nameBild)
	plt.savefig(nameBild+'.pdf')
	plt.gcf().clear()
	return result


def compare_array_2_number(array = [], number = 1, greaterOrLess = 0):
	#greaterOrLess = 0 means array > number
	#greaterOrLess = 1 means array < number
	#greaterOrLess = 1 means array <= number
	result = np.zeros(len(array))
	if greaterOrLess == 0:
		for i in range(0,len(result)):
			if array[i] > number:
				result[i] = 1
	else :
		if greaterOrLess == 1:
			for i in range(0,len(result)):
				if array[i] < number:
					result[i] = 1
		else:
			if greaterOrLess == 2 :
				for i in range(0,len(result)):
					if array[i] <= number:
						result[i] = 1
			else:
				print('The parameter greaterOrLess is invalid, should be either 0 or 1')
				sys.exit()
	return result
def matlab_min(array1,array2):
	if len(array1)!=len(array2):
		print('Error: the two given arrays should have the same length')
		sys.exit()
	result = np.zeros(len(array1))
	for i in range (0,len(result)):
		result[i] = min (array1[i],array2[i])
	return result
def matlab_max(array1,array2):
	if len(array1)!=len(array2):
		print('Error: the two given arrays should have the same length')
		sys.exit()
	result = np.zeros(len(array1))
	for i in range (0,len(result)):
		result[i] = max (array1[i],array2[i])
	return result
def matlab_get_true_indexes(array):
	res = []
	for i in range (0,len(array)):
		if array[i]==1:
			res.append(i)
	return res
def matlab_update_array(array,indexes,values):
	result = array
	if len(indexes)!= len(values):
		print('Error: indexes- and values array must have the same length')
		sys.exit()
	for i in range(0,len(indexes)):
		result[indexes[i]] = values[i]
	return array
def matlab_get_subarray(array,indexes):
	result = []
	for i in indexes :
		result.append(array[i])
	return result
def power(my_list,n):
	return [ x**n for x in my_list ]
def key2float(s):
	sub1 = s[:s.index('.')+1]
	sub2 = s[(s.index('.')+1):]
	sub2 = sub2.replace('.','')
	result = sub1 + sub2
	return float(result)

if __name__ == '__main__':
	# Initialization of colored text output:
	colorama.init()
	copyright_message = "copyright_message: Still to be determined"
	# Parse the command line arguments:
	parser = argparse.ArgumentParser(description=copyright_message+'This tool is a python version of Verzerrungszahlen.m.' + ' ' + version_string + '.')

	#Reading the parameters
	parser.add_argument('-i', action="store", dest="input_file", required=True, help='Name of input file.')
	parser.add_argument('-signal', action="store", dest="signal", required=True, help='Name of the output file generated from singlesine_Signal.')
	parser.add_argument('-ref', action="store", dest="sineref", required=True, help='Name of the output file generated from singlesine_SineRef.')
	parser.add_argument('-o', action="store", dest="output_file", required=True, help='Name of output file.')
	parser.add_argument('-frev', action="store", dest="frev", required=True, help='Wiederholfrequenz.')
	parser.add_argument('-fBB', action="store", dest="fBB", required=True, help='Barier-Bucket-Frequenz.')
	parser.add_argument('--debug', action="store_true", dest="debug", default=False, help='This switch enables the debug mode.')
	parser.add_argument('-csv', action="store", dest="csv", default=False, help='This switch enables the generation of an output file in csv format.')

	parse_result = parser.parse_args(sys.argv[1:])
	flag = parse_result.input_file
	output_file = parse_result.output_file
	signal = parse_result.signal
	sineref = parse_result.sineref
	frev = float(parse_result.frev)
	fBB = float(parse_result.fBB)
	debug = parse_result.debug
	csv = int(parse_result.csv)

	print(colorama.Back.GREEN + colorama.Style.BRIGHT + "singlesine_Verzerrungszahlen: Start." + colorama.Style.NORMAL + colorama.Back.RESET)

	"""
	#Reading first input file
	# --signal
	# Read input file
	print("Processing file: " + signal)
	print("Reading data...")
	# If flag_read_all is set to True, the header and the complete content of the file are loaded into memory. Else, only the header information is read.
	fin = rftools_bcf.ReadBCF(signal, flag_read_all=True)
	if not fin.flag_file_opened:
		print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: Failed reading file " + signal + ", exit."+ colorama.Style.NORMAL + colorama.Back.RESET)
		# Return code for error (failed reading input file):
		sys.exit(20)
	if not fin.flag_read_valid:
		print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: Failed reading file " + signal + ", exit."+ colorama.Style.NORMAL + colorama.Back.RESET)
		# Return code for error (failed reading input file):
		sys.exit(21)
	print("Finished reading data")
	if fin.flag_empty_file:
		print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: Empty file " + signal + ", exit."+ colorama.Style.NORMAL + colorama.Back.RESET)
		# Return code for error (empty input file):
		sys.exit(22)

	#New Error
	if fin.number_of_columns < 4:
		print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: Number of columns is not sufficient (smaller than 4) " + signal + ", exit."+ colorama.Style.NORMAL + colorama.Back.RESET)
		# Return code for error (empty input file):
		sys.exit(21)

	dataPointsSignal = fin.return_data(segment_nr=0, column_nr=3, start_row=0, end_row=-1, step=1)
	if len (np.where(np.isnan(dataPointsSignal))[0]) > 0 :
		dataPointsSignal = dataPointsSignal[0:np.where(np.isnan(dataPointsSignal))[0][0]]
	"""


	input_file = read_csv(signal)
	dataPointsSignal = np.array(input_file.values[:,3][3:]).astype(np.float)

	if len(np.where(np.isnan(dataPointsSignal))[0]) != 0:
		dataPointsSignal = dataPointsSignal[0:np.where(np.isnan(dataPointsSignal))[0][0]]

	"""
	#Reading second output file
	# --ref
	print("Processing file: " + sineref)
	print("Reading data...")
	# If flag_read_all is set to True, the header and the complete content of the file are loaded into memory. Else, only the header information is read.
	fin = rftools_bcf.ReadBCF(sineref, flag_read_all=True)
	if not fin.flag_file_opened:
		print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: Failed reading file " + sineref + ", exit."+ colorama.Style.NORMAL + colorama.Back.RESET)
		# Return code for error (failed reading input file):
		sys.exit(20)
	if not fin.flag_read_valid:
		print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: Failed reading file " + sineref + ", exit."+ colorama.Style.NORMAL + colorama.Back.RESET)
		# Return code for error (failed reading input file):
		sys.exit(21)
	print("Finished reading data")
	if fin.flag_empty_file:
		print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: Empty file " + sineref + ", exit."+ colorama.Style.NORMAL + colorama.Back.RESET)
		# Return code for error (empty input file):
		sys.exit(22)

	#New Error
	if fin.number_of_columns < 5:
		print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: Number of columns is not sufficient (smaller than 5) " + sineref + ", exit."+ colorama.Style.NORMAL + colorama.Back.RESET)
		# Return code for error (empty input file):
		sys.exit(21)

	dataPointsRef = fin.return_data(segment_nr=0, column_nr=0, start_row=0, end_row=-1, step=1)
	if len (np.where(np.isnan(dataPointsSignal))[0]) > 0 :
		dataPointsRef = dataPointsRef[0:np.where(np.isnan(dataPointsSignal))[0][0]]

	PulseOn = fin.return_data(segment_nr=0, column_nr=1, start_row=0, end_row=-1, step=1)
	if len (np.where(np.isnan(PulseOn))[0]) > 0 :
		PulseOn = PulseOn[0:np.where(np.isnan(PulseOn))[0][0]]
	PointsPulse = fin.return_data(segment_nr=0, column_nr=2, start_row=0, end_row=-1, step=1)[0]
	PulseA = fin.return_data(segment_nr=0, column_nr=3, start_row=0, end_row=-1, step=1)[0]
	PulseP = fin.return_data(segment_nr=0, column_nr=4, start_row=0, end_row=-1, step=1)[0]
	"""

	input_file = read_csv(sineref)
	PointsPulse = float(input_file.values[:,1][3])#
	PulseA = float(input_file.values[:,2][3])#
	PulseP = float(input_file.values[:,4][3])#
	dataPointsRef = np.array(input_file.values[:,5][3:]).astype(np.float)#
	PulseOn = np.array(input_file.values[:,3][3:]).astype(np.float)#
	#plt.plot(dataPointsRef)
	#plt.show()


	res = Verzerrungszahlen(dataPointsRef,dataPointsSignal,PulseOn,PointsPulse,PulseA,PulseP,frev,fBB,flag)
	if debug:
		print('Debugging mode activated')
		print(res)

	#Write output_file

	if "." in output_file:
		flag = output_file.split('.')[0]
	else:
		flag = output_file
	#d = dict(dataPointsRef = dataPointsRef,PointsPulse = PointsPulse,PulseA = PulseA,PulseP = PulseP,PulseOn = PulseOn)
	d = res
	d['Name'] = parse_result.input_file
	df = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in d.items() ]))


	# get count of header columns, add REAL for each one
	types_header_for_insert = list(df.columns.values)
	for idx, val in enumerate(types_header_for_insert):
		types_header_for_insert[idx] = ' '


	# count number of index columns, then add STRING for each one
	index_count = len(df.index.names)
	for idx in range(0, index_count):
		df.reset_index(level=0, inplace=True)
		types_header_for_insert.insert(0, ' ')

	column_information = [[0,0,1,x] for x in d.keys()]
	temp = [x[3] for x in column_information]
	temp.remove('Name')
	temp.sort()
	temp.insert(0, 'Name')
	#temp = [temp[-1]] + temp[:-1]
	df = df[temp]


	#temp.insert(0, ' ')

	#temp[-1],temp[-2],temp[-3],temp[-4],temp[-5] = temp[-5],temp[-1],temp[-4],temp[-2],temp[-3]
	df.loc[-1]  = temp
	temp = [x[0] for x in column_information]
	#temp.insert(0, ' ')
	#temp[-1],temp[-2],temp[-3],temp[-4],temp[-5] = temp[-5],temp[-1],temp[-4],temp[-2],temp[-3]
	df.loc[-2]  = temp
	temp = [x[1] for x in column_information]
	#temp.insert(0, ' ')
	#temp[-1],temp[-2],temp[-3],temp[-4],temp[-5] = temp[-5],temp[-1],temp[-4],temp[-2],temp[-3]
	df.loc[-3]  = temp
	#temp = ['','Column file','columns={}'.format(len(column_information)),'rows={}'.format(len(t)),'generated by singlesinge_Signal',' ']
	temp = [' ' for x in temp]
	temp[0:4] = ['Column file','columns={}'.format(len(column_information)),'rows={}'.format(1),'generated by singlesine_Verzerrungszahlen']
	df.loc[-4]  = temp

	#sort index
	df = df.sort_index()
	print('%s is written'%(flag+'.csv'))
	temp = [x[3] for x in column_information]
	#df.to_csv(flag+'.csv',index=False,header=False)
#	print('%s is written'%output_file)
	df.to_csv(flag+'.csv',index=False,header=False)

	#Write the BCF output file
	"""
	output_string = flag + ".bcf"
	# This is the current time in steps of 100 nanoseconds (cf. the document with the definition of the BCF file format):
	time_stamp = time.time()*1e7
	header_description = 'Generated by SINGLESINE_VERZERRUNGSZAHLEN'
	keys_string = 'device=SINGLESINE_VERZERRUNGSZAHLEN'

	column_information = [[0,0,1,x] for x in res.keys()]
	# This calls the constructor of the WriteBCF class:
	outfile = rftools_bcf.WriteBCF(output_string, time_stamp, header_description, keys_string, column_information)
	# First write the header:
	outfile.write_header()
	# Now write the segments:
	relative_time = 0
	x = np.array(list(res.values()))
	x = x.reshape((1,len(x)))

	outfile.write_segment(relative_time*1e7, x)
	# Write the keys, this finishes the file:
	outfile.write_keys()
	#Success
	print("Output file " + output_string + " has been written.")
	if csv == 1 :
		os.system("python rfconvert_bcf2csv.py -i {} -o {} -d 1".format(output_string,flag+".csv"))
	"""
	print(colorama.Back.GREEN + colorama.Style.BRIGHT + "singlesine_Verzerrungszahlen: Done." + colorama.Style.NORMAL + colorama.Back.RESET)
	print('\n')
	# Return code 0 (success):
	sys.exit(0)

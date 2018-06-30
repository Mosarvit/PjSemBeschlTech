#!/usr/bin/python3
#@author: Mohamed Ghanmi
from __future__ import division

version_string = 'Rev. 0.0.4, 19.06.2018'

import rftools_bcf
import pandas as pd
from pandas import read_csv
import numpy as np
import matplotlib.pyplot as plt
import fractions
from scipy.interpolate import interp1d
from math import ceil,floor
import sys, os,glob, argparse, colorama, time

# Documentation data for Doxygen
## @package singlesine_Signal.py
# Calculates the discrete Fourier transform of a sampled signal (ti, yi)
#
#
# \param[in] -h Help switch.
# \param[in] -i Name of input file.
# \param[in] -frev Wiederholfrequenz.
# \param[in] -fBB Barier-Bucket-Frequenz.
# \param[in] -o Name of output file.
# \param[out] Integer number as error code (0: success, 1: general error, 10: error due to input parameters, 20: error while reading an input file, 21: input file has incorrect file format, 22: input file is empty, 30: error while writing the output file, 31: output file already exists)

def pad(array, length):
	if len(array) == length:
		return array
	array = np.append(array,np.nan*np.ones(length - len(array)))
	return array

def Signal_reshape(Startindex,Vorzeichen,t,dataPointsSignal):
	max_length = max([len(t),len(dataPointsSignal)])
	Startindex = pad([Startindex],max_length)
	Vorzeichen = pad([Vorzeichen],max_length)
	t = pad(t,max_length)
	dataPointsSignal = pad(dataPointsSignal,max_length)

	return np.stack((Startindex,Vorzeichen,t,dataPointsSignal),axis = -1)
def lcm(a,b): return abs(a * b) / fractions.gcd(a,b) if a and b else 0
def key2float(s):
	sub1 = s[:s.index('.')+1]
	sub2 = s[(s.index('.')+1):]
	sub2 = sub2.replace('.','')
	result = sub1 + sub2
	return float(result)

def Einlesen (dateiName,folderName,SingleSine):

	if folderName != "":
		if folderName == "csvDateien_K" :
			"""
			************************************
			Einlesen der csv-Dateien von Kerstin
			************************************
			"""
			t = SingleSine.values[:,0]
			t = np.insert(t, 0, key2float(np.array(SingleSine.keys())[0]), axis=0)
			messignal = SingleSine.values[:,1]
			messignal = np.insert(messignal, 0, key2float(np.array(SingleSine.keys())[1]), axis=0)
			# Einlesen der Messinformationen
			t_Sample = t[1] - t[0]
			HOffset = t[0]
			tShift = t - HOffset

		if folderName in ["csvDateien_M","csvDateien_J3dB"] :
			"""
			************************************
			Einlesen der csv-Dateien von Michael
			************************************
			"""
			t = SingleSine.values[:,3]
			messignal = SingleSine.values[:,4]
			# Einlesen der Messinformationen
			#Anzahl gemessener Punkte
			NPunkte = int(np.array(SingleSine.keys())[1])
			#Abtastzeit Messung
			t_Sample = float(SingleSine.values[0,1])
			TriggerPoint = float(SingleSine.values[1,1])
			HOffset = float(SingleSine.values[4,1])
			tShift = t - HOffset
	else:
		shape = SingleSine.shape
		msg = SingleSine.keys()[1]
		if 'device=RFGEN_SINGLESINE' in msg:
			t = np.array(SingleSine.values[3:,0])
			t = np.array([x.replace(" ", "") for x in t ]).astype(np.float)
			#print(len(t))
			messignal = np.array(SingleSine.values[3:,1]).astype(np.float)
			t_Sample = t[1] - t[0]
			#Automatic insertion of a new point
			t = np.insert(t,0,t[0]-t_Sample,axis = 0)
			messignal = np.insert(messignal,0,0,axis = 0)
			###
			HOffset = t[0]
			tShift = t - HOffset


		else:
			if len(shape) == 2 and shape[1] == 2:
				t = SingleSine.values[3:,0]
				t = np.array(t)
				t = np.array([x.replace(" ", "") for x in t ]).astype(np.float)
				print(t)
				messignal = np.array(SingleSine.values[3:,1]).astype(np.float)
				# Einlesen der Messinformationen
				t_Sample = t[1] - t[0]
				HOffset = t[0]
				tShift = t - HOffset
			else:
				print('shape of input file',SingleSine.shape)
				print("Falsche Formatierung der Eingabedatei")
				sys.exit()

	return t,messignal,t_Sample,HOffset,tShift

def Signal(dateiName,frev,fBB):
	"""
	Einlesen und Signalaufbereitung des gemessenen Einzelsinus
	Ausgabe
	Die Punkte pro eine Periode
	Eingabe
	Dateiname, Wiederholfrequenz und Barier-Bucket-Frequenz
	"""
	folderName = "";
	if "/" in dateiName:
		folderName = dateiName.split("/")[0]

	print('Processing the file %s' %dateiName)
	filetype = dateiName.split(".")[1]

	if filetype == "csv":
		SingleSine = read_csv(dateiName)
		t,messignal,t_Sample,HOffset,tShift = Einlesen(dateiName,folderName,SingleSine)
	elif filetype == "bcf":

		# Read input file
		print("Processing file: " + dateiName)
		print("Reading data...")
		# If flag_read_all is set to True, the header and the complete content of the file are loaded into memory. Else, only the header information is read.
		fin = rftools_bcf.ReadBCF(dateiName, flag_read_all=True)
		if not fin.flag_file_opened:
			print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: Failed reading file " + dateiName + ", exit."+ colorama.Style.NORMAL + colorama.Back.RESET)
			# Return code for error (failed reading input file):
			sys.exit(20)
		if not fin.flag_read_valid:
			print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: Failed reading file " + dateiName + ", exit."+ colorama.Style.NORMAL + colorama.Back.RESET)
			# Return code for error (failed reading input file):
			sys.exit(21)
		print("Finished reading data")
		if fin.flag_empty_file:
			print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: Empty file " + idateiName + ", exit."+ colorama.Style.NORMAL + colorama.Back.RESET)
			# Return code for error (empty input file):
			sys.exit(22)
		#New Error
		if fin.number_of_columns < 2:
			print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: Number of columns is not sufficient (smaller than 2) " + dateiName + ", exit."+ colorama.Style.NORMAL + colorama.Back.RESET)
			# Return code for error (empty input file):
			sys.exit(21)

		t = fin.return_data(segment_nr=0, column_nr=0, start_row=0, end_row=-1, step=1)
		if len (np.where(np.isnan(t))[0]) > 0 :
			t = dataPointsSignal[0:np.where(np.isnan(t))[0][0]]

		messignal = fin.return_data(segment_nr=0, column_nr=1, start_row=0, end_row=-1, step=1)
		if len (np.where(np.isnan(messignal))[0]) > 0 :
			messignal = messignal[0:np.where(np.isnan(messignal))[0][0]]
		t_Sample = t[1] - t[0]
		HOffset = t[0]
		tShift = t - HOffset
	else:
		print("Unknown type of input file. The tool can either process csv or bcf input files.")
		sys.exit()

	"""
	 Berechnen einer neuen Abtastzeit, so dass sowohl der Puls, als auch
	 eine Periode des ganzen Signals ganzzahlige Anzahl von Abtastintervale
	 haben und die Shanon-Theorem erfuellt ist
	"""
	PointsMin=round((1/frev)/(1/(lcm(2*frev,2*fBB))))
	t_Sample_Neu=(1/frev)/PointsMin #minimale Abtastzeit
	while t_Sample_Neu >t_Sample:
		t_Sample_Neu /= 2
	PointsPerPeriod=int((1/frev)/t_Sample_Neu) #Punkte pro Periode bei der neuen Abtastfrequenz (muss ein Ganzahl sein)
	tNeu = np.arange(0,tShift[-1],t_Sample_Neu)
	#tNeu = np.arange(0,tShift[-1],t_Sample_Neu+t_Sample)
	tShift [0] = 0

	#Interpolation function f_interp
	f_interp = interp1d(tShift, messignal, kind='linear')
	dataPoints = f_interp(tNeu)#Abtasten des Signals mit der neuen Frequenz
	#Checking for NaNs
	for x in dataPoints:
		if (np.isnan(x)):
			print(colorama.Back.RED + colorama.Style.BRIGHT +'myApp:argChk'+'Die Interpolation in Zeile 69 ist fehlgeschlagen, tNeu muss in dem Intervall [0,tShift(end)] sein.'+colorama.Style.NORMAL + colorama.Back.RESET)
			#sys.exit()?
			break

	#Mittelung der Signal ueber die Periodenanzahl
	nPeriod = int(ceil (len(dataPoints)/PointsPerPeriod))#Anzahl der aufgenommenen Perioden nach oben gerundet
	SignalMatrix = np.zeros(nPeriod*PointsPerPeriod)
	SignalMatrix = np.reshape(SignalMatrix,(nPeriod,PointsPerPeriod))

	#VERY IMPORTANT: POSSIBLE MEMORY ERROR DUE TO RAM LIMITS
	if len(dataPoints) < PointsPerPeriod:
		print(colorama.Back.RED + colorama.Style.BRIGHT + "myApp:argChk', 'Es wurde keine ganze Periode aufgenommen. Bitte ueberprefen Sie ob die Wiederhol- und Barrier-Bucket-Frequenz in der Eingabedatei stimmen."+ colorama.Style.NORMAL + colorama.Back.RESET)
	else:
		if nPeriod == 1:
			SignalMatrix = np.reshape(SignalMatrix,(PointsPerPeriod,nPeriod))
		else:
			SignalMatrix_Hilfs= np.reshape(dataPoints[0:(nPeriod-1)*PointsPerPeriod],(PointsPerPeriod,nPeriod-1),order='F')
			SignalMatrix[0:nPeriod-1,:]=np.transpose(SignalMatrix_Hilfs)

	 # die Letzte Periode im Allgemeinen unvollstaendig. Die fehlende Werte
	 # werden mit den Werten vom vorherigen Periode aufgefuellt
	if nPeriod > 1 :
		end = len(dataPoints) - 1
		SignalMatrix[nPeriod-1,:] = np.append(dataPoints[(nPeriod-1)*PointsPerPeriod:end],dataPoints[end-PointsPerPeriod:(nPeriod-1)*PointsPerPeriod])
		dataPointsSignal= SignalMatrix.mean(0) #Datenpunkte fuer eine Periode
	else:
		SignalMatrix = np.reshape(SignalMatrix,(PointsPerPeriod,nPeriod))
		dataPointsSignal= dataPoints

	pointsPulse=1/(fBB*t_Sample_Neu)
	min_value = min(dataPointsSignal)
	index_min = int(np.where(dataPointsSignal == min_value)[0][0])
	max_value = max(dataPointsSignal)
	index_max = int(np.where(dataPointsSignal == max_value)[0][0])
	index_end = int(len(dataPointsSignal)-1)

	#Bestimmen, ob zuerst das Minimum oder das Maximum kommt
	if index_min<index_max:
		index_1 = index_min
		index_2 = index_max
	else:
		index_1 = index_max
		index_2 = index_min


	if frev/fBB>0.6432:
		end = len (dataPointsSignal) - 1
		print('Die Frequenzen fBB und frev liegen nah bei einander. Es kann zu Probleme beim generieren des Signals kommen. Schauen Sie sich das generierte Bild im Bilder Ordner .')
		plotDataPointsSignal = 1
		startphase=int(round(0.8*pointsPulse))
		if index_1 - startphase >= 0:
			dataPointsSignalES = np.append(dataPointsSignal[index_1-startphase :end + 1],dataPointsSignal[0:index_1-startphase])
			Startindex = index_1 - startphase
		else:
			dataPointsSignalES = np.append(dataPointsSignal [end+(index_1-startphase):end + 1],dataPointsSignal[0:end+(index_1-startphase)])
			Startindex = len(dataPointsSignal) + (index_1-startphase)

	else:
		end = len (dataPointsSignal) - 1
		plotDataPointsSignal = 0
		startphase = int(round(0.8*pointsPulse))
		if index_1 - startphase >= 0:
			dataPointsSignalES = np.append(dataPointsSignal[index_1-startphase :end + 1],dataPointsSignal[0:index_1-startphase])
			Startindex = index_1 - startphase
		else:
			dataPointsSignalES = np.append(dataPointsSignal[end+(index_1-startphase):end + 1],dataPointsSignal[0:end+(index_1-startphase)])
			Startindex = len(dataPointsSignal) + (index_1-startphase)


	min_valueES = min(dataPointsSignalES)
	index_minES = int(np.where(dataPointsSignalES == min_valueES)[0][0])
	max_valueES = max(dataPointsSignalES)
	index_maxES = int(np.where(dataPointsSignalES == max_valueES)[0][0])


	#Bestimmen, ob zuerst das Minimum oder das Maximum kommt
	if index_minES < index_maxES:
		Vorzeichen = -1
	else:
		Vorzeichen = 1

	result  = dataPointsSignalES,Vorzeichen,Startindex,tNeu,plotDataPointsSignal
	return result

if __name__ == "__main__":
	# Initialization of colored text output:
	colorama.init()
	copyright_message = "copyright_message: Still to be determined"
	# Parse the command line arguments:
	parser = argparse.ArgumentParser(description=copyright_message+'This tool is a python version of Signal.m.' + ' ' + version_string + '.')

	#Reading the parameters
	parser.add_argument('-i', action="store", dest="input_file", required=True, help='Name of input file.')
	parser.add_argument('-o', action="store", dest="output_file", required=True, help='Name of output file.')
	parser.add_argument('-frev', action="store", dest="frev", required=True, help='Wiederholfrequenz.')
	parser.add_argument('-fBB', action="store", dest="fBB", required=True, help='Barier-Bucket-Frequenz.')
	parser.add_argument('-csv', action="store", dest="csv", default=False, help='This switch enables the generation of an output file in csv format.')
	parser.add_argument('--debug', action="store_true", dest="debug", default=0, help='This switch enables the debug mode (0 or 1).')

	parse_result = parser.parse_args(sys.argv[1:])
	frev = float(parse_result.frev)
	fBB = float(parse_result.fBB)
	debug = parse_result.debug
	csv = int(parse_result.csv)

	print(colorama.Back.GREEN + colorama.Style.BRIGHT + "singlesine_Signal: Start." + colorama.Style.NORMAL + colorama.Back.RESET)

	input_file = parse_result.input_file
	output_file = parse_result.output_file

	dataPointsSignal,Vorzeichen,Startindex,t,plotDataPointsSignal = Signal(input_file,frev,fBB)

	if debug or plotDataPointsSignal == 1:
		plt.plot(dataPointsSignal,linewidth=0.4)
		print('Debugging mode activated')
		print('Vorzeichen = %s'%Vorzeichen)
		print('Startindex = %s'%Startindex)
		print('t = %s'%t)
		plt.show()

	if "." in output_file:
		flag = output_file.split('.')[0]
	else:
		flag = output_file

	d = dict( t = t, Vorzeichen = Vorzeichen,Startindex = Startindex, dataPointsSignal = dataPointsSignal)
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


	#set new value to dataframe
	#temp = [' ' for x in types_header_for_insert]
	column_information = [(0, 0, 1, 'Startindex'),(0, 0, 1, 'Vorzeichen'), (6, 6, 1, 't'), (103, 3, 1, 'dataPointsSignal') ]


	temp = [x[3] for x in column_information]
	temp.insert(0, ' ')
	temp[-1],temp[-2] = temp[-2],temp[-1]
	df.loc[-1]  = temp
	temp = [x[0] for x in column_information]
	temp.insert(0, ' ')
	temp[-1],temp[-2] = temp[-2],temp[-1]
	df.loc[-2]  = temp
	temp = [x[1] for x in column_information]
	temp.insert(0, ' ')
	temp[-1],temp[-2] = temp[-2],temp[-1]
	df.loc[-3]  = temp
	temp = ['','Column file','columns={}'.format(len(column_information)),'rows={}'.format(len(t)),'generated by singlesinge_Signal']
	df.loc[-4]  = temp

	#sort index
	df = df.sort_index()
	print('%s is written'%(flag + '.csv'))
	df.to_csv(flag + '.csv',index=False,header=False)


	"""
	#Write the BCF output file


	output_string = flag + ".bcf"
	# This is the current time in steps of 100 nanoseconds (cf. the document with the definition of the BCF file format):
	time_stamp = time.time()*1e7
	header_description = 'Generated by SINGLESINE_SIGNAL'
	keys_string = 'device=SINGLESINE_SIGNAL'
	column_information = [(0, 0, 1, 'Startindex'),(0, 0, 1, 'Vorzeichen'), (6, 6, 1, 't/s'), (103, 3, 1, 'y/V') ]
	# This calls the constructor of the WriteBCF class:
	outfile = rftools_bcf.WriteBCF(output_string, time_stamp, header_description, keys_string, column_information)
	# First write the header:
	outfile.write_header()
	# Now write the segments:
	relative_time = 0
	x = Signal_reshape(Startindex,Vorzeichen,t,dataPointsSignal)
	outfile.write_segment(relative_time*1e7, x)
	# Write the keys, this finishes the file:
	outfile.write_keys()
	#Success
	print("Output file " + output_string + " has been written.")

	if csv == 1 :
		os.system("python rfconvert_bcf2csv.py -i {} -o {} -d 1".format(output_string,flag+".csv"))
	print(colorama.Back.GREEN + colorama.Style.BRIGHT + "singlesine_Signal: Done." + colorama.Style.NORMAL + colorama.Back.RESET)
	# Return code 0 (success):
	sys.exit(0)
	"""

#!/usr/bin/python3
#@author: Mohamed Ghanmi
from __future__ import division

version_string = 'Rev. 0.0.3, 15.06.2018'
import tools.rftools_bcf
import pandas as pd
from pandas import read_csv
import numpy as np
from numpy import fft
import scipy.optimize
import sys, os, glob, argparse, colorama, time
import matplotlib.pyplot as plt
from tools.singlesine_Signal import pad

# Documentation data for Doxygen
## @package singlesine_SineRef.py
# Calculates the discrete Fourier transform of a sampled signal (ti, yi)
#
#
# \param[in] -h Help switch.
# \param[in] -i Name of input file.
# \param[in] -frev Wiederholfrequenz.
# \param[in] -fBB Barier-Bucket-Frequenz.
# \param[in] -o Name of output file.
# \param[out] Integer number as error code (0: success, 1: general error, 10: error due to input parameters, 20: error while reading an input file, 21: input file has incorrect file format, 22: input file is empty, 30: error while writing the output file, 31: output file already exists)

def SineRef_reshape(dataPointsRef,PointsPulse,PulseOn,PulseA,PulseP):
	max_length = max([len(dataPointsRef),len(PulseOn)])
	dataPointsRef = pad(dataPointsRef,max_length)
	PulseOn = pad(PulseOn,max_length)
	PointsPulse = pad([PointsPulse],max_length)
	PulseA = pad([PulseA],max_length)
	PulseP = pad([PulseP],max_length)

	return np.stack((dataPointsRef,PulseOn,PointsPulse,PulseA,PulseP),axis = -1)

def power(my_list,n):
	return [ x**n for x in my_list ]

def SineRef(frev,fBB,dataPointsSignal,Vorzeichen,Startindex):
	"""
	Generieren des Referenz-Einzelsinus
	Ausgabe
	Abgtastetes Referenzsignal, Anzahl der Abtastpunkte des Pulses
	Eingabe
	Wiederholfrequenz und Barier-Bucket-Frequenz, Anzahl der
	Abstastpunkte pro Periode;
	Phase des Einzelpulses
	"""
	# Fehler hier bei rgsinglesine !!!!!!
	Y = fft.fft(dataPointsSignal)/len(dataPointsSignal)
	# end
	B_wbb_wrev = 2*abs(Y[int(np.fix(fBB/frev))])
	#plt.plot(abs(Y))
	#plt.show()

	Amplitude=Vorzeichen*B_wbb_wrev*(fBB/frev)



	t_Sample=(1/frev)/len(dataPointsSignal) #Abtastzeit
	t = np.arange(0,1/fBB,t_Sample)
	pulse=Amplitude*np.sin(2*np.pi*fBB*t) #Generieren des Pulses



	PointsPerPeriod = len(dataPointsSignal)# Punkte pro Periode

	#plt.plot(dataPointsSignal-np.mean(dataPointsSignal))
	#plt.plot(pulse,'r')
	#plt.show()

	acor = np.correlate(dataPointsSignal-np.mean(dataPointsSignal), pulse, mode = 'full')
	#Generate an x axis
	lag = np.arange(acor.size)
	#Convert this into lag units, but still not really physical
	lag -= (pulse.size-1)
	#IMPORTANT CHECK LAG AND ACOR VECTORS

	hilfvar = max (acor)
	I = int(np.where(acor == hilfvar)[0][0])
	lagDiff = lag[I]

	t = np.arange(0,1/fBB,t_Sample)

	if lagDiff >= 0:
		func = lambda var : sum(power(var[0]*np.append(np.zeros(lagDiff),np.append(np.sin(2*np.pi*fBB*t+var[1]),np.zeros(PointsPerPeriod-lagDiff-len(pulse)))) - dataPointsSignal,2))
		TolFun = 1e-10
		TolX = 1e-6
		opt = scipy.optimize.fmin(func=func, x0=[Amplitude,0],disp = False,xtol=TolX, ftol=TolFun)
		fval  = func (opt)
	else:
		print(colorama.Back.RED + colorama.Style.BRIGHT + 'Erorr:','myApp:argChk', 'Problem beim Erstellen des Signal: dataPointsSignal. Bitte Ueberpruefen Sie, ob die Wiederhol- und Barrier-Bucket-Frequenz in der Eingabedatei stimmen.'+colorama.Style.NORMAL + colorama.Back.RESET)


	#plt.plot(pulse ,label='pulse')
	#plt.plot(dataPointsSignal,label='dataPointsSignal')
	#plt.legend()
	#plt.show()
	## DEBUG:
	#print(opt)
	#sys.exit()


	dataPointsRef = opt[0] * np.append(np.append(np.zeros(abs(lagDiff)),np.sin(2*np.pi*fBB*t+opt[1])),np.zeros(PointsPerPeriod-abs(lagDiff)-len(pulse)))
	PointsPulse = len(pulse)
	PulseOn = np.append(np.append(np.zeros(abs(lagDiff)),np.ones (len(pulse))) , np.zeros(PointsPerPeriod-abs(lagDiff)-len(pulse)))
	PulseA=opt[0]*800
	PulseP=((Startindex+abs(lagDiff))/PointsPerPeriod-opt[1]/2/np.pi/fBB*frev)*360;

	result  = dataPointsRef,PointsPulse,PulseOn,PulseA,PulseP
	return result

if __name__ == '__main__':

	# Initialization of colored text output:
	colorama.init()
	copyright_message = "copyright_message: Still to be determined"
	# Parse the command line arguments:
	parser = argparse.ArgumentParser(description=copyright_message+'This tool is a python version of SineRef.m.' + ' ' + version_string + '.')

	#Reading the parameters
	parser.add_argument('-i', action="store", dest="input_file", required=True, help='Name of input file.')
	parser.add_argument('-o', action="store", dest="output_file", required=True, help='Name of output file.')
	parser.add_argument('-frev', action="store", dest="frev", required=True, help='Wiederholfrequenz.')
	parser.add_argument('-fBB', action="store", dest="fBB", required=True, help='Barier-Bucket-Frequenz.')
	parser.add_argument('--debug', action="store_true", dest="debug", default=False, help='This switch enables the debug mode.')
	parser.add_argument('-csv', action="store", dest="csv", default=False, help='This switch enables the generation of an output file in csv format.')

	parse_result = parser.parse_args(sys.argv[1:])
	frev = float(parse_result.frev)
	fBB = float(parse_result.fBB)
	debug = parse_result.debug
	csv = int(parse_result.csv)

	print(colorama.Back.GREEN + colorama.Style.BRIGHT + "singlesine_SineRef: Start." + colorama.Style.NORMAL + colorama.Back.RESET)

	input_file = parse_result.input_file
	output_file = parse_result.output_file


	# Read input file
	"""
	print("Processing file: " + input_file)
	print("Reading data...")
	# If flag_read_all is set to True, the header and the complete content of the file are loaded into memory. Else, only the header information is read.
	fin = rftools_bcf.ReadBCF(input_file, flag_read_all=True)
	if not fin.flag_file_opened:
		print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: Failed reading file " + input_file + ", exit."+ colorama.Style.NORMAL + colorama.Back.RESET)
		# Return code for error (failed reading input file):
		sys.exit(20)
	if not fin.flag_read_valid:
		print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: Failed reading file " + input_file + ", exit."+ colorama.Style.NORMAL + colorama.Back.RESET)
		# Return code for error (failed reading input file):
		sys.exit(21)
	print("Finished reading data")
	if fin.flag_empty_file:
		print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: Empty file " + input_file + ", exit."+ colorama.Style.NORMAL + colorama.Back.RESET)
		# Return code for error (empty input file):
		sys.exit(22)

	#New Error
	if fin.number_of_columns < 4:
		print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: Number of columns is not sufficient (smaller than 4) " + input_file + ", exit."+ colorama.Style.NORMAL + colorama.Back.RESET)
		# Return code for error (empty input file):
		sys.exit(21)


	Startindex = fin.return_data(segment_nr=0, column_nr=0, start_row=0, end_row=0, step=1)[0]
	Vorzeichen = fin.return_data(segment_nr=0, column_nr=1, start_row=0, end_row=0, step=1)[0]
	t = fin.return_data(segment_nr=0, column_nr=2, start_row=0, end_row=-1, step=1)
	if len (np.where(np.isnan(t))[0]) > 0 :
		t = dataPointsSignal[0:np.where(np.isnan(t))[0][0]]
	dataPointsSignal = fin.return_data(segment_nr=0, column_nr=3, start_row=0, end_row=-1, step=1)
	if len (np.where(np.isnan(dataPointsSignal))[0]) > 0 :
		dataPointsSignal = dataPointsSignal[0:np.where(np.isnan(dataPointsSignal))[0][0]]

	"""

	#Reading input file
	input_file = read_csv(input_file)
	#print(input_file)
	Startindex = int(float(input_file.values[:,1][3]))
	Vorzeichen = int(float(input_file.values[:,2][3]))
	dataPointsSignal = np.array(input_file.values[:,3][3:]).astype(np.float)

	if len(np.where(np.isnan(dataPointsSignal))[0]) != 0:
		dataPointsSignal = dataPointsSignal[0:np.where(np.isnan(dataPointsSignal))[0][0]]

	t = np.array(input_file.values[:,4][3:]).astype(np.float)

	dataPointsRef,PointsPulse,PulseOn,PulseA,PulseP = SineRef(frev,fBB,dataPointsSignal,Vorzeichen,Startindex)

	if debug:
		plt.plot(dataPointsSignal, label='dataPointsSignal')
		plt.plot(dataPointsRef, label = 'dataPointsRef')
		print('Debugging mode activated')
		print('PointsPulse = %s'%PointsPulse)
		plt.plot(PulseOn * np.max(dataPointsRef),label = 'PulseOn * dataPointsRef_max')
		print('PulseA = %s'%PulseA)
		print('PulseP = %s'%PulseP)
		plt.legend()
		plt.show()

	#Write the BCF output file
	if "." in output_file:
		flag = output_file.split('.')[0]
	else:
		flag = output_file

	column_information = [(103, 3, 1, 'dataPointsRef'), (0, 0, 1, 'PulseOn'),(0, 0, 1, 'PointsPulse'),(0, 0, 1, 'PulseA'), (0, 0, 1, 'PulseP') ]

	d = dict(dataPointsRef = dataPointsRef,PulseOn = PulseOn,PointsPulse = PointsPulse,PulseA = PulseA,PulseP = PulseP,)
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

	temp = [x[3] for x in column_information]
	temp.insert(0, ' ')
	temp[-1],temp[-2],temp[-3],temp[-4],temp[-5] = temp[-5],temp[-1],temp[-4],temp[-2],temp[-3]
	df.loc[-1]  = temp
	temp = [x[0] for x in column_information]
	temp.insert(0, ' ')
	temp[-1],temp[-2],temp[-3],temp[-4],temp[-5] = temp[-5],temp[-1],temp[-4],temp[-2],temp[-3]
	df.loc[-2]  = temp
	temp = [x[1] for x in column_information]
	temp.insert(0, ' ')
	temp[-1],temp[-2],temp[-3],temp[-4],temp[-5] = temp[-5],temp[-1],temp[-4],temp[-2],temp[-3]
	df.loc[-3]  = temp
	temp = ['','Column file','columns={}'.format(len(column_information)),'rows={}'.format(len(dataPointsRef)),'generated by singlesinge_Signal',' ']
	df.loc[-4]  = temp

	#sort index
	df = df.sort_index()
	print('%s is written'%(flag+'.csv'))
	temp = [x[3] for x in column_information]
	df.to_csv(flag+'.csv',index=False,header=False)



	"""
	output_string = flag + ".bcf"
	# This is the current time in steps of 100 nanoseconds (cf. the document with the definition of the BCF file format):
	time_stamp = time.time()*1e7
	header_description = 'Generated by SINGLESINE_SINEREF'
	keys_string = 'device=SINGLESINE_SINEREF'
	column_information = [(103, 3, 1, 'dataPointsRef/V'), (0, 0, 1, 'PulseOn'),(0, 0, 1, 'PointsPulse'),(0, 0, 1, 'PulseA'), (0, 0, 1, 'PulseP') ]
	# This calls the constructor of the WriteBCF class:
	outfile = rftools_bcf.WriteBCF(output_string, time_stamp, header_description, keys_string, column_information)
	# First write the header:
	outfile.write_header()
	# Now write the segments:
	relative_time = 0
	x = SineRef_reshape(dataPointsRef,PointsPulse,PulseOn,PulseA,PulseP)
	outfile.write_segment(relative_time*1e7, x)
	# Write the keys, this finishes the file:
	outfile.write_keys()
	#Success
	print("Output file " + output_string + " has been written.")

	if csv == 1 :
		os.system("python rfconvert_bcf2csv.py -i {} -o {} -d 1".format(output_string,flag+".csv"))
	"""
	print(colorama.Back.GREEN + colorama.Style.BRIGHT + "singlesine_SineRef: Done." + colorama.Style.NORMAL + colorama.Back.RESET)
	# Return code 0 (success):
	sys.exit(0)

#!/usr/bin/python3
#@author: Mohamed Ghanmi
from __future__ import division


version_string = 'Rev. 0.0.2, 15.06.2018'
import rftools_bcf
import colorama, argparse, sys, os, time
import pandas as pd
import numpy as np
from singlesine_Signal import Signal
from singlesine_SineRef import SineRef
from singlesine_Verzerrungszahlen import Verzerrungszahlen



def Bewertung(flag,fBB,frev):
	#dateiName = "csvDateien_M/" + flag + ".csv"
	dateiName = flag
	dataPointsSignal,Vorzeichen,Startindex,t,plotDataPointsSignal = Signal(dateiName,frev,fBB)
	dataPointsRef,PointsPulse,PulseOn,PulseA,PulseP = SineRef(frev,fBB,dataPointsSignal,Vorzeichen,Startindex)
	result = Verzerrungszahlen(dataPointsRef,dataPointsSignal,PulseOn,PointsPulse,PulseA,PulseP,frev,fBB,flag)
	result['Name'] = flag
	result['frev'] = frev
	result['fBB'] = fBB

	return result

if __name__ == "__main__":
	# Initialization of colored text output:
	colorama.init()
	copyright_message = "copyright_message: Still to be determined"
	# Parse the command line arguments:
	parser = argparse.ArgumentParser(description=copyright_message+'This tool is a python version of Bewertung.m.' + ' ' + version_string + '.')

	#Reading the parameters
	parser.add_argument('-f', action="store", dest="flag", required=True, help='flag of input file.')
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

	print(colorama.Back.GREEN + colorama.Style.BRIGHT + "singlesine_Bewertung: Start." + colorama.Style.NORMAL + colorama.Back.RESET)

	flag = parse_result.flag
	output_file = parse_result.output_file

	#print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: for file + " + filename + ", the input and output file names are identical, skipping this file."+ colorama.Style.NORMAL + colorama.Back.RESET)

#    frev = 9e5
#    fBB = 5e6

	res = Bewertung(flag,fBB,frev)

	if debug:
		print('Debugging mode activated')
		print(res)
		#print('Testing result2row')
		#row = result2row(result)
		#print(row)


	#d = dict(dataPointsRef = dataPointsRef,PointsPulse = PointsPulse,PulseA = PulseA,PulseP = PulseP,PulseOn = PulseOn)
	d = res
	df = pd.DataFrame(dict([ (k,pd.Series(v)) for k,v in d.items() ]))
	print('%s is written'%output_file)
	df.to_csv(output_file)


	"""
	#Write the BCF output file
	if "." in output_file:
		flag = output_file.split('.')[0]
	else:
		flag = output_file

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
	x = np.array(res.values())
	x = x.reshape((1,len(x)))
	#LENNA W9EFT
	outfile.write_segment(relative_time*1e7, x)
	# Write the keys, this finishes the file:
	outfile.write_keys()
	#Success
	print("Output file " + output_string + " has been written.")
	if csv == 1 :
		os.system("python rfconvert_bcf2csv.py -i {} -o {} -d 1".format(output_string,flag+".csv"))
	"""
	print(colorama.Back.GREEN + colorama.Style.BRIGHT + "singlesine_Bewertung: Done." + colorama.Style.NORMAL + colorama.Back.RESET)
	print('\n')
	# Return code 0 (success):
	sys.exit(0)
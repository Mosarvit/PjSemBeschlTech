#!/usr/bin/python3
#@author: Mohamed Ghanmi
from __future__ import division
import sys ,os, colorama, argparse
from tools.singlesine_Bewertung import Bewertung

import pandas as pd
version_string = 'Rev. 0.0.1, 06.06.2018'

def Eingabedatei(Ueberschreiben,input_file,folder_name):
	fname = 'Ergebnisse.xls'
	dname = 'Bilder'

	if Ueberschreiben == 1:
		if os.path.isfile(fname):
			os.system("rm {}".format(fname))
			fname = 'Ergebnisse.csv'
			os.system("rm {}".format(fname))
		if os.path.isdir(dname):
			os.system("rm -rf {}".format(dname))

	file = open(input_file,"r")
	flags = []
	f_REVs = []
	f_BBs= []

	#TODO: IGNORE EMPTY LINES

	data = file.read().split("\n")
	if '' in data:
		data.remove('')

	for i in range(1,len(data)):
		temp = data[i]
		#print('DEBUG')
		#print(temp)
		#replacing 2 spaces with inly one space
		temp.replace("  "," ")
		temp = temp.split(" ")
		if '' in temp:
			temp.remove('')
		#print('DEBUG')
		#print(temp)
		flags.append(temp[0])
		f_REVs.append(temp[1])
		f_BBs.append(temp[2])

	flags = [folder_name+ '/' + x +'.csv' for x in flags]
	f_REVs = [float(x) for x in f_REVs]
	f_BBs = [float(x) for x in f_BBs]



	#print(f_BBs)
	keys = ['Name','f_rev','f_BB','Amplitude', 'Phase', 'deltaGesamtVar1', 'deltaPulseVar1', 'MWpulseVar1', 'deltaRestVar1','maxPulseVar1','maxRestVar1',
		'deltaGesamtVar2', 'deltaPulseVar2', 'MWpulseVar2', 'deltaRestVar2', 'maxPulseVar2','maxRestVar2',
		'deltaGesamtVar3', 'deltaPulseVar3', 'MWpulseVar3', 'deltaRestVar3', 'maxPulseVar3','maxRestVar3',
		'deltaGesamtVar4', 'deltaPulseVar4', 'MWpulseVar4', 'deltaRestVar4', 'maxPulseVar4','maxRestVar4']

	output_pd = pd.DataFrame(columns=keys)
	#print(flags)
	for i in range(0,len(flags)):
		flag = flags[i]
		fBB = f_BBs[i]
		frev = f_REVs[i]

		#print('DEBUG')
		#print(type(f_BBs[i]))

		if fBB < frev:
			print('myApp:argChk', 'Die Barrier-Bucket-Frequenz muss groesser sein, als die Wiederholfrequenz.')
		else:
			result = Bewertung(flag,fBB,frev)
			row = result2row(result)
			row[0] = row[0].split("/")[-1].split(".")[0]
			output_pd.loc[i] = row
	return output_pd




def result2row(result):

	row = [result['Name'], result['frev'], result['fBB'],result['Amplitude'], result['Phase'], result['QGesamt1'],
		result['Qpulse1'], result['MWpulse1'], result['Qrest1'],result['maxPulse1'],result['maxRest1'],
		result['QGesamt2'], result['Qpulse2'], result['MWpulse2'], result['Qrest2'], result['maxPulse2'],result['maxRest2'],
		result['QGesamt3'], result['Qpulse3'], result['MWpulse3'], result['Qrest3'],result['maxPulse3'],result['maxRest3'],
		result['QGesamt4'], result['Qpulse4'], result['MWpulse4'], result['Qrest4'],result['maxPulse4'],result['maxRest4']]

	return row

if __name__ == "__main__":
	# Initialization of colored text output:
	colorama.init()
	copyright_message = "copyright_message: Still to be determined"
	# Parse the command line arguments:
	parser = argparse.ArgumentParser(description=copyright_message+'This tool is a python version of Eingabedatei.m.' + ' ' + version_string + '.')

	#Reading the parameters
	parser.add_argument('-i', action="store", dest="input_file", required=True, help='Name of input file.')
	parser.add_argument('-f', action="store", dest="folder_name", required=True, help='Name of the folder where the csv files are saved.')
	parser.add_argument('-u', action="store", dest="overwrite", required=True, help='specifies whether existing files should be overwritten.')

	parse_result = parser.parse_args(sys.argv[1:])


	print(colorama.Back.GREEN + colorama.Style.BRIGHT + "singlesine_EingabeDatei: Start." + colorama.Style.NORMAL + colorama.Back.RESET)

	input_file = parse_result.input_file
	folder_name = parse_result.folder_name
	overwrite = int(parse_result.overwrite)
	#print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: for file + " + filename + ", the input and output file names are identical, skipping this file."+ colorama.Style.NORMAL + colorama.Back.RESET)


	resulting_panda = Eingabedatei(overwrite,input_file,folder_name)

	#if debug:
	#	print('Debugging mode activated')
	#	print(result)
		#print('Testing result2row')
		#row = result2row(result)
		#print(row)


	#d = dict(dataPointsRef = dataPointsRef,PointsPulse = PointsPulse,PulseA = PulseA,PulseP = PulseP,PulseOn = PulseOn)

	print('Ergebnisse.csv is written')


	if not os.path.isfile('Ergebnisse.xls'):
		resulting_panda.to_csv('Ergebnisse.csv')
		writer = pd.ExcelWriter('Ergebnisse.xls')
		resulting_panda.to_excel(writer,'Sheet1')
		writer.save()
	else:
		result = pd.read_csv('Ergebnisse.csv',names = ['Name','f_rev','f_BB','Amplitude', 'Phase', 'deltaGesamtVar1', 'deltaPulseVar1', 'MWpulseVar1', 'deltaRestVar1','maxPulseVar1','maxRestVar1',
			'deltaGesamtVar2', 'deltaPulseVar2', 'MWpulseVar2', 'deltaRestVar2', 'maxPulseVar2','maxRestVar2',
			'deltaGesamtVar3', 'deltaPulseVar3', 'MWpulseVar3', 'deltaRestVar3', 'maxPulseVar3','maxRestVar3',
			'deltaGesamtVar4', 'deltaPulseVar4', 'MWpulseVar4', 'deltaRestVar4', 'maxPulseVar4','maxRestVar4'])
		result = pd.concat([result,resulting_panda],ignore_index=True)
		result.to_csv('Ergebnisse.csv')
		writer = pd.ExcelWriter('Ergebnisse.xls')
		result.to_excel(writer,'Sheet1')
		writer.save()


	print(colorama.Back.GREEN + colorama.Style.BRIGHT + "singlesine_EingabeDatei: Done." + colorama.Style.NORMAL + colorama.Back.RESET)
	print('\n')
	# Return code 0 (success):
	sys.exit(0)

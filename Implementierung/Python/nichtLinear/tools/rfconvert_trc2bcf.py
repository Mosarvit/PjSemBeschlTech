#!/usr/bin/python3
# GSI-PBRF (D. Lens)
revision_string = '0.1.9, 26.09.2017'

import rftools_misc, rftools_bcf, rftools_trc
import sys, glob, argparse, colorama
import time, datetime
import numpy as np

# Initialization of colored text output:
colorama.init()

# Parse the command line arguments:
parser = argparse.ArgumentParser(description='RF tools, RFCONVERT_TRC2BCF. Converts one or more LeCroy Trace file(s) (TRC) to a binary column file (BCF). Revision: ' + revision_string + '.')
parser.add_argument('-i', action="store", dest="input_file", required=True, help='Name of input file(s). Wildcards such as * and [0-9] may be used.')
parser.add_argument('-o', action="store", dest="output_file", default='', help='Name of output file. For multiple input files, this string is appended to the input file names.')
parser.add_argument('-t', action="store", dest="data_type", default='0', help='Specifies the data type that is used to save the data: 0 (float), 1 (double). Default is 0.')

parse_result = parser.parse_args(sys.argv[1:])

print(colorama.Back.GREEN + colorama.Style.BRIGHT + "RFCONVERT_TRC2BCF: Start." + colorama.Style.NORMAL + colorama.Back.RESET)

# Check parameters:
output_string = parse_result.output_file

# Wildcard expansion for the input file list:
file_list = glob.glob(parse_result.input_file)
if not file_list:
	print(colorama.Back.YELLOW + colorama.Style.BRIGHT + "RFCONVERT_TRC2BCF: Input file list is empty, nothing to do."+ colorama.Style.NORMAL + colorama.Back.RESET)
	raise SystemExit()


# Iterate through file list:
for filename in file_list:
	fin = rftools_trc.ReadTRC(filename)
	if not fin.flag_read_valid:
		print(colorama.Back.RED + colorama.Style.BRIGHT + "RFCONVERT_TRC2BCF ERROR: file + " + filename + " could not be read, skipping this file."+ colorama.Style.NORMAL + colorama.Back.RESET)
		continue
	
	# Prepare output file
	if len(file_list) == 1:
		if output_string == '':
			if filename[-4:] == '.trc':
				output_filename = filename[:-4] + '.bcf'
			else:
				output_filename = filename + '.bcf'
		else:
			if output_string[-4:] == '.bcf':
				output_filename = output_string
			else:
				output_filename = output_string + '.bcf'
	else:
		if filename[-4:] == '.trc':
			output_filename = filename[:-4] + output_string + '.bcf'
		else:
			output_filename = filename + output_string + '.bcf'

	if output_filename == filename:
		print(colorama.Back.RED + colorama.Style.BRIGHT + "RFCONVERT_TRC2BCF ERROR: for file + " + filename + ", the input and output file names are identical, skipping this file."+ colorama.Style.NORMAL + colorama.Back.RESET)
		continue
	
	header_description_string = 'Created by RFCONVERT_TRC2BCF (rev. ' + revision_string + ')'
	
	column_information = []
	if parse_result.data_type == '1':
		column_information.append((6,6, 1, "t/s"))	 # First column is a time variable
		column_information.append((3,103, 1, "Voltage " + fin.wave_source + "/V" )) # Second column is a voltage variable
	else:	
		column_information.append((6,6, 0, "t/s"))	 # First column is a time variable
		column_information.append((3,103, 0, "Voltage " + fin.wave_source + "/V" )) # Second column is a voltage variable

	time_stamp = time.mktime( (datetime.datetime.strptime(fin.time_of_measurement[1:-5],"%Y-%m-%d %H:%M:%S")).timetuple() ) * 1e7
	time_stamp += (int(fin.time_of_measurement[-4:-1])) * 1e4 # Also take the sub-second part into account (three digits after the seconds-comma)
	
	keys_string = ''
	keys_string += "grouping='none'"
	keys_string += "device='" + fin.instrument_name + "'"
	
	fout = rftools_bcf.WriteBCF(output_filename,time_stamp,header_description_string,keys_string,column_information,fin.number_of_segments)
	
	for segment_cnt in range(0, fin.number_of_segments):
		# Read the complete segment:
		print("Reading segment " + str(segment_cnt+1) + "                ", end="\r")
		fin.read_next_segment()
		print("Writing segment " + str(segment_cnt+1) + "                ", end="\r")
		# Write the complete segment:
		fout.write_segment(fin.t_abs*1e7, np.column_stack((fin.t_rel,fin.y)))
		
	fout.write_keys()
	print('RFCONVERT_TRC2BCF: file ' + output_filename + ' has been written')


print(colorama.Back.GREEN + colorama.Style.BRIGHT + "RFCONVERT_TRC2BCF: Done." + colorama.Style.NORMAL + colorama.Back.RESET)

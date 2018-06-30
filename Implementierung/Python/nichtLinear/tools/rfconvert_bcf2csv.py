#!/usr/bin/python3
# GSI-PBRF (D. Lens)
revision_string = '0.1.0, 04.10.2017'

import rftools_misc, rftools_bcf, rftools_csv
import sys, glob, argparse, colorama
import time, datetime
import numpy as np

# Initialization of colored text output:
colorama.init()

# Parse the command line arguments:
parser = argparse.ArgumentParser(description='RF tools, RFCONVERT_BCF2CSV. Converts one or more binary column files (BCF) in text column file(s) (CSV). Only the first segment of the BCF is converted, any further segments are ignored. Revision: ' + revision_string + '.')
parser.add_argument('-i', action="store", dest="input_file", required=True, help='Name of input file(s). Wildcards such as * and [0-9] may be used.')
parser.add_argument('-o', action="store", dest="output_file", required=True, help='Name of output file. For multiple input files, this string is appended to the input file names.')
parser.add_argument('-d', action="store", dest="delimiter", default='0', help='Defines the delimiter symbol for the CSV file: 0 (comma), 1 (tabulator). Default is tabulator.')
parser.add_argument('-t', action="store", dest="type", default='0', help='Defines the type of the CSV file: 0 (Column File), 1 (2D File). Default is 0. For the 2D File, the BCF must have 2 columns (x = first column, z = second column) or 3 columns (x, y, z).')
parse_result = parser.parse_args(sys.argv[1:])

print(colorama.Back.GREEN + colorama.Style.BRIGHT + "RFCONVERT_BCF2CSV: Start." + colorama.Style.NORMAL + colorama.Back.RESET)

# Check parameters:
output_string = parse_result.output_file

try:
	csv_type = int(parse_result.type)
except:
	print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: Invalid input parameter for the CSV type (conversion to integer failed), exit."+ colorama.Style.NORMAL + colorama.Back.RESET)
	sys.exit(10)
if not csv_type in [0,1]:
	print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: Invalid input parameter for the CSV type (valid values are: 0, 1), exit."+ colorama.Style.NORMAL + colorama.Back.RESET)
	sys.exit(10)
	

# Wildcard expansion for the input file list:
file_list = glob.glob(parse_result.input_file)
if not file_list:
	print(colorama.Back.YELLOW + colorama.Style.BRIGHT + "ERROR: Input file list is empty, nothing to do."+ colorama.Style.NORMAL + colorama.Back.RESET)
	sys.exit(10)

delimiter_symbol = parse_result.delimiter
if delimiter_symbol == '0':
	delimiter = ', '
elif delimiter_symbol == '1':
	delimiter = '\t'
else:
	print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: invalid delimiter symbol." + colorama.Style.NORMAL + colorama.Back.BLACK)
	sys.exit(10)


# Iterate through file list:
for filename in file_list:

	print("Processing file " + filename)
	# Read BCF file:
	fin = rftools_bcf.ReadBCF(filename)
	if not fin.flag_read_valid:
		print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: file + " + filename + " could not be read, skipping this file."+ colorama.Style.NORMAL + colorama.Back.RESET)
		continue
	
	x = np.ndarray((fin.segment_number_of_rows[0],fin.number_of_columns))
	for col_cnt in range(0,fin.number_of_columns):
		x[:,col_cnt] = fin.return_data(0, col_cnt)
			
	# Prepare output file
	if len(file_list) == 1:
		output_filename = output_string
	else:
		output_filename = filename + output_string
	if output_filename == filename:
		print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: for file + " + filename + ", the input and output file names are identical, skipping this file."+ colorama.Style.NORMAL + colorama.Back.RESET)
		continue

	if not output_filename[-4:] == '.csv':
		output_filename += '.csv'

	header_description_string = 'Created by RFCONVERT_BCF2CSV'
	column_information = fin.column_information
				
	# Write output file:
	# Column File
	if csv_type == 0:

		type_list = []
		unit_list = []
		comment_list = []
		for col_cnt in range(0, fin.number_of_columns):
			type_list.append(fin.column_information[col_cnt][0])
			unit_list.append(fin.column_information[col_cnt][1])
			comment_list.append(fin.column_information[col_cnt][3])					
		further_keys = []
		further_keys.append('segment_number=' + str(1))
		temp = rftools_misc.get_key_value(fin.keys_string,'segment_time','string')
		if temp:
			further_keys.append('segment_time=' + temp)
		else:
			further_keys.append('segment_time=' + str(fin.segment_times_in_100ns[0]/1e7))
		grouping = rftools_misc.get_key_value(fin.keys_string,'grouping','string')
		device = rftools_misc.get_key_value(fin.keys_string,'device','string')
		user_name = rftools_misc.get_key_value(fin.keys_string,'user_name','string')
			
		fout = rftools_csv.WriteCSV(output_filename)
		fout.write_column_file(type_list, unit_list, comment_list, x, delimiter, further_keys, True, "'" + fin.time_stamp_string + "'", grouping, device, user_name)


	# 2D File
	elif csv_type == 1:

		if not fin.number_of_columns in [2,3]:
			print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: For csv type 1 (2D file), the number of columns must be 2 or 3. This is not the case for the current file, skipping this file."+ colorama.Style.NORMAL + colorama.Back.RESET)
			continue		
		
		if fin.number_of_columns == 2:
			type_list = [fin.column_information[0][0], 0, fin.column_information[1][0]]
			unit_list = [fin.column_information[0][1], 0, fin.column_information[1][1]]
			xyz_comment_list = [fin.column_information[0][3], 'Undefined', fin.column_information[1][3]]
			X = fin.return_data(segment_nr=0, column_nr=0)
			Z = fin.return_data(segment_nr=0, column_nr=1)
			Y = np.array([0])
								
		elif fin.number_of_columns == 3:				
			type_list = [fin.column_information[0][0], fin.column_information[1][0], fin.column_information[2][0]]
			unit_list = [fin.column_information[0][1], fin.column_information[1][1], fin.column_information[2][1]]
			xyz_comment_list = [fin.column_information[0][3], fin.column_information[1][3], fin.column_information[2][3]]
			# Read data (xi, yi, zi)
			xi = fin.return_data(segment_nr=0, column_nr=0)
			yi = fin.return_data(segment_nr=0, column_nr=1)
			zi = fin.return_data(segment_nr=0, column_nr=2)
			# Determine the unique, sorted values of x and y:
			X = np.unique(xi)
			Y = np.unique(yi)
			# Now construct the Z matrix:
			Z = np.empty((len(X),len(Y)))
			Z.fill(np.nan)
			for cnt in range(0,len(xi)):
				Xind = np.where(X==xi[cnt])[0][0]
				Yind = np.where(Y==yi[cnt])[0][0]
				Z[Xind,Yind] = zi[cnt]
			if np.isnan(Z).any():
				print(colorama.Back.YELLOW + colorama.Style.BRIGHT + "WARNING: There are z-values that are not defined (not a number) in the output file."+ colorama.Style.NORMAL + colorama.Back.RESET)
		
		fout = rftools_csv.WriteCSV(output_filename)
		fout.write_2D_file(type_list, unit_list, xyz_comment_list, X, Y, Z, delimiter, overwrite=True)
		
			
	print('RFCONVERT_BCF2CSV: file ' + output_filename + ' has been written')

print(colorama.Back.GREEN + colorama.Style.BRIGHT + "RFCONVERT_BCF2CSV: Done." + colorama.Style.NORMAL + colorama.Back.RESET)
sys.exit(0)

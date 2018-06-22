#!/usr/bin/python3
# STARFISH-PY: Software Tools for Accelerator RF Instrumentation via Command Shell using Python

version_string = 'Rev. 0.1.2, 14.05.2018'

#    STARFISH-PY, PLOT2D: Waterfall plot.
#    Copyright (C) 2015-2018  GSI, D. Lens

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.

## @package PLOT2D.py
# Plots two-dimensional data.
#
# Plots binary column files with one x-column and one y-column as a waterfall plot.
#
# \param[in] -h Help switch.
# \param[in] -i Name of input file(s). Multiple file name can be specified by using commas without leading or trailing space, e.g. "-i a.bcf,b.bcf". Alternatively, wildcards (Unix style) can be used.
# \param[in] -x Column with x-values to be displayed. Default value is 0 (index) for files with one column and 1 (first column) for files with more than one column. Choose 0 to plot versus the index of the y-column.
# \param[in] -y Column with y-values to be displayed. Default value is 1 (first column) for files with one column and 2 (second column) for files with more than one column.
# \param[in] --reverse Turns the waterfall plot upside-down.
# \param[in] --SIunits If this option is used, all values are plotted in SI units. Else, an automatic scaling of the values is tried.
# \param[in] --deg If this switch is used, a phase value is plotted as degree and not as radian.
# \param[out] Integer number as error code (0 on sucess)

import numpy as np
import lib.rftools_misc as rftools_misc
import lib.rftools_bcf as rftools_bcf
import sys, glob, argparse, colorama
import matplotlib.pyplot as plt

# Initialization of colored text output:
colorama.init()

# Parse the command line arguments:
parser = argparse.ArgumentParser(description='RF tools, PLOT2D. Makes a graphical, two-dimensional (waterfall) plot of binary column files with 2 columns, ' + version_string + '.')
parser.add_argument('-i', action="store", dest="input_file", required=True, help='Name of input file(s). Multiple file name can be specified by using commas without leading or trailing space, e.g. "-i a.bcf,b.bcf". Alternatively, wildcards (Unix style) can be used.')
parser.add_argument('-x', action="store", dest="x_column", default='-1', help="Column with x-values to be displayed. Default value is 0 (index) for files with one column and 1 (first column) for files with more than one column. Choose 0 to plot versus the index of the y-column.")
parser.add_argument('-y', action="store", dest="y_column", default='-1', help='Column with y-values to be displayed. Default value is 1 (first column) for files with one column and 2 (second column) for files with more than one column.')
parser.add_argument('--reverse', action="store_true", dest="reverse", default=False, help='Turns the waterfall plot upside-down.')
parser.add_argument('--SIunits', action="store_true", dest="SI", default=False, help='If this option is used, all values are plotted in SI units. Else, an automatic scaling of the values is tried.')
parser.add_argument('--deg', action="store_true", dest="use_degree", default=False, help='If this switch is used, a phase value is plotted as degree and not as radian.')
parse_result = parser.parse_args(sys.argv[1:])

print(colorama.Back.GREEN + colorama.Style.BRIGHT + "PLOT2D: Start." + colorama.Style.NORMAL + colorama.Back.RESET)

# Check parameters:
flag_invalid_xcol = False
x_column_list = []
try:
	nx = len(parse_result.x_column.split(','))
	if nx == 1:
		x_column_list.append(int(parse_result.x_column))
	else:
		flag_invalid_xcol = True
except:
	flag_invalid_xcol = True
if flag_invalid_xcol:
	print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: Invalid input parameter " +parse_result.x_column+ " for the column of x-values (integer conversion failed), exit."+ colorama.Style.NORMAL + colorama.Back.RESET)
	sys.exit(10)
try:
	y_column = int(parse_result.y_column)
except:
	print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: Invalid input parameter " +parse_result.y_column+ " for the column of y-values (integer conversion failed), exit."+ colorama.Style.NORMAL + colorama.Back.RESET)
	sys.exit(10)

# Wildcard expansion for the input file list:
file_list = []
for item in parse_result.input_file.split(","):
	file_list.extend(glob.glob(item))
if not file_list:
	print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: Empty input file list, nothing to do."+ colorama.Style.NORMAL + colorama.Back.RESET)
	sys.exit(10)

for file_cnt in range(0,len(file_list)):
	
	filename = file_list[file_cnt]
	
	# Read input file
	print("RFPLOT: Processing file: " + filename)
	print("  Reading data...")
	fin = rftools_bcf.ReadBCF(filename, True)
	if fin.flag_read_valid:
		print("  Finished reading data")
	else:
		print(colorama.Back.RED + colorama.Style.BRIGHT + "  ERROR: Failed reading file " + filename + ", exit."+ colorama.Style.NORMAL + colorama.Back.RESET)
		# Return code for error (failed reading input file):
		sys.exit(21)
	if fin.flag_empty_file or fin.number_of_segments < 1:
		print(colorama.Back.RED + colorama.Style.BRIGHT + "  Empty file " + filename + ", exit."+ colorama.Style.NORMAL + colorama.Back.RESET)
		# Return code for error (empty input file):
		sys.exit(22)

	maximum_number_of_rows = int(max(fin.segment_number_of_rows))
	minimum_number_of_rows = int(min(fin.segment_number_of_rows))
	
	print("  Number of segments: " + str(fin.number_of_segments))
	print("  Number of columns: " + str(fin.number_of_columns))

	if fin.number_of_segments == 1:
		print("  Number of rows: " + str(minimum_number_of_rows))
	else:
		print("  Minimum number of rows: " + str(minimum_number_of_rows))
		print("  Maximum number of rows: " + str(maximum_number_of_rows))
		print(colorama.Back.YELLOW + colorama.Style.BRIGHT + "  Warning: For the x-column of the waterfall plot, the x-values of the first segment will be used. It will be assumed that they are also valid for the other segments."+ colorama.Style.NORMAL + colorama.Back.RESET)
		
	# Set default values:
	for cnt in range(0,len(x_column_list)):
		if x_column_list[cnt] == -1:
			if fin.number_of_columns == 1:
				x_column_list[cnt] = 0
			else:
				x_column_list[cnt] = 1			
			
		if x_column_list[cnt] > fin.number_of_columns or x_column_list[cnt] < 0:
			print(colorama.Back.RED + colorama.Style.BRIGHT + "  ERROR: Specified column for the x-values is invalid for this file. Choose a value between 1 and " + str(fin.number_of_columns) + ". This file is skipped." + colorama.Style.NORMAL + colorama.Back.RESET)
			continue

	if y_column == -1:
		if fin.number_of_columns == 1:
			y_column = 1
		else:
			y_column = 2
			
	if y_column > fin.number_of_columns or y_column < 1:
		print(colorama.Back.RED + colorama.Style.BRIGHT + "  ERROR: Specified column for the y-values is invalid for this file. Choose a value between 1 and " + str(fin.number_of_columns) + ". This file is skipped." + colorama.Style.NORMAL + colorama.Back.RESET)
		continue

	if not minimum_number_of_rows == maximum_number_of_rows:
		print(colorama.Back.YELLOW + colorama.Style.BRIGHT + "  WARNING: The number of rows is not the same for all segments. Missing samples will be plotted in white color." + colorama.Style.NORMAL + colorama.Back.RESET)
			
	x_column = x_column_list[0]
	Z = np.full((fin.number_of_segments,maximum_number_of_rows), np.nan)
	for seg_cnt in range(0, fin.number_of_segments):
		temp = fin.return_data(seg_cnt,y_column-1)					
		if parse_result.reverse:		
			Z[fin.number_of_segments-seg_cnt-1,0:len(temp)] = temp
		else:
			Z[seg_cnt,0:len(temp)] = temp			
		
	# limits of the y-axis of the plot:
	y_lower_limit = 1
	y_upper_limit = fin.number_of_segments
	# limits of the x-axis of the plot
	fig, ax = plt.subplots()
	if x_column > 0:
		x = fin.return_data(0, x_column-1)
		if len(x) < 2:
			x_column = 0
			print(colorama.Back.YELLOW + colorama.Style.BRIGHT + "  WARNING: The first segment has less than 2 rows. Therefore, the data is plotted versus the index." + colorama.Style.NORMAL + colorama.Back.RESET)
		else:									
			x_lower_limit = x[0]					
			sample_time = x[1] - x[0]					
			x_upper_limit = x_lower_limit + sample_time * (maximum_number_of_rows-1)
			if parse_result.SI:
				x_column_string = fin.column_information[x_column-1][3][:]
			else:
				x_factor, x_column_string = rftools_misc.auto_unit_conversion(fin.column_information[x_column-1][1], fin.column_information[x_column-1][3][:], max(abs(x_upper_limit),abs(x_lower_limit)), parse_result.use_degree)
				x_lower_limit, x_upper_limit = x_lower_limit * x_factor, x_upper_limit * x_factor
		
	if x_column == 0:
		x_column_string = 'Index'
		x_lower_limit = 0
		x_upper_limit = maximum_number_of_rows-1
			
	if parse_result.SI:
		z_column_string = fin.column_information[y_column-1][3][:]
	else:
		z_factor, z_column_string = rftools_misc.auto_unit_conversion(fin.column_information[y_column-1][1], fin.column_information[y_column-1][3][:], np.max((abs(Z))), parse_result.use_degree)
	Z = Z * z_factor	
	
	if parse_result.reverse:
		cax = ax.imshow(Z, interpolation='none',aspect='auto',extent=[x_lower_limit,x_upper_limit,y_lower_limit,y_upper_limit])
	else:
		cax = ax.imshow(Z, interpolation='none',aspect='auto',extent=[x_lower_limit,x_upper_limit,y_upper_limit,y_lower_limit])		
	cbar = fig.colorbar(cax, shrink=0.4, aspect=10)#, ticks=[-1, 0, 1])
	ax.set_xlabel(x_column_string, fontsize=14, color='blue')
	ax.set_ylabel('Segment No.', fontsize=14, color='blue')
	plt.title(z_column_string, fontsize=14, color='blue')		

# Success:
plt.show()
print(colorama.Back.GREEN + colorama.Style.BRIGHT + "PLOT2D: Done." + colorama.Style.NORMAL + colorama.Back.BLACK)
sys.exit(0)

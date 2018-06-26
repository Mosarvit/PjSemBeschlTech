#!/usr/bin/python3
# STARFISH-PY: Software Tools for Accelerator RF Instrumentation via Command Shell using Python

version_string = 'Rev. 0.4.1, 14.05.2018'

#    STARFISH-PY, PLOT: Plots one-dimensional data.
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

## @package PLOT.py
# Plots one-dimensional data.
#
# Plots binary column files with one x-column and one y-column. If the input file has several segments, only the first row of each segment is used.
#
# \param[in] -h Help switch.
# \param[in] -i Name of input file(s). Multiple file name can be specified by using commas without leading or trailing space, e.g. "-i a.bcf,b.bcf". Alternatively, wildcards (Unix style) can be used.
# \param[in] -x Column with x-values to be displayed. Default value is 0 (index) for files with one column and 1 (first column) for files with more than one column. Choose 0 to plot versus the index of the y-column.
# \param[in] -y Column with y-values to be displayed. Default value is 1 (first column) for files with one column and 2 (second column) for files with more than one column.
# \param[in] -l Specifies the line style. Available styles are: 0 (points only at data points), 1 (solid line), 2 (dashed), 3 (dotted), 4 (dash-dotted). Default is 0. For multiple plots in one figure, several numbers separated by commas may be used to specify the line style for each plot, e.g.: "-l 0,1,2".
# \param[in] -m Specifies the marker style. Available styles are: 0 (no marker), 1 (circle), 2 (star), 3 (square), 4 (triangle down), 5 (triangle up). Default is 0. For multiple plots in one figure, several numbers separated by commas may be used to specify the line style for each plot, e.g.: "-m 0,1,2".
# \param[in] --one_figure Plot all input files in one figure.
# \param[in] --SIunits Use SI units.
# \param[in] --deg Use degree for phase values.
# \param[out] Integer number as error code (0 on sucess)

import numpy as np
import lib.rftools_misc as rftools_misc
import lib.rftools_bcf as rftools_bcf
import sys, glob, argparse, colorama
import matplotlib.pyplot as plt

# Initialization of colored text output:
colorama.init()

copyright_message = "STARFISH-PY, PLOT  Copyright (C) 2017  D. Lens. This program comes with ABSOLUTELY NO WARRANTY; This is free software, and you are welcome to redistribute it under certain conditions; see 'LICENCE' for details. "

# Parse the command line arguments:
parser = argparse.ArgumentParser(description='RF tools, PLOT. Makes a graphical, one-dimensional plot of binary column files with 2 columns, ' + version_string + '.')
parser.add_argument('-i', action="store", dest="input_file", required=True, help='Name of input file(s). Multiple file name can be specified by using commas without leading or trailing space, e.g. "-i a.bcf,b.bcf". Alternatively, wildcards (Unix style) can be used.')
parser.add_argument('-x', action="store", dest="x_column", default='-1', help="Column with x-values to be displayed. Default value is 0 (index) for files with one column and 1 (first column) for files with more than one column. Choose 0 to plot versus the index of the y-column.")
parser.add_argument('-y', action="store", dest="y_column", default='-1', help='Column with y-values to be displayed. Default value is 1 (first column) for files with one column and 2 (second column) for files with more than one column.')
parser.add_argument('-l', action="store", dest="linestyle", default='0', help='Specifies the line style. Available styles are: 0 (points only at data points), 1 (solid line), 2 (dashed), 3 (dotted), 4 (dash-dotted). Default is 0. For multiple plots in one figure, several numbers separated by commas may be used to specify the line style for each plot, e.g.: "-l 0,1,2".')
parser.add_argument('-m', action="store", dest="markerstyle", default='0', help='Specifies the marker style. Available styles are: 0 (no marker), 1 (circle), 2 (star), 3 (square), 4 (triangle down), 5 (triangle up). Default is 0. For multiple plots in one figure, several numbers separated by commas may be used to specify the line style for each plot, e.g.: "-m 0,1,2".')
parser.add_argument('--one_figure', action="store_true", dest="flag_display_in_one_figure", default=False, help='If this option is used, all specified input files are plotted in one figure. If not (default), each input file is plotted in a new figure.')
parser.add_argument('--SIunits', action="store_true", dest="SI", default=False, help='If this option is used, all values are plotted in SI units. Else, an automatic scaling of the values is tried.')
parser.add_argument('--deg', action="store_true", dest="use_degree", default=False, help='If this switch is used, a phase value is plotted as degree and not as radian.')
parse_result = parser.parse_args(sys.argv[1:])

print(colorama.Back.GREEN + colorama.Style.BRIGHT + "PLOT: Start." + colorama.Style.NORMAL + colorama.Back.RESET)

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
	print(colorama.Back.RED + colorama.Style.BRIGHT + "PLOT ERROR: Invalid input parameter " +parse_result.x_column+ " for the column of x-values (integer conversion failed), exit."+ colorama.Style.NORMAL + colorama.Back.RESET)
	sys.exit(10)
try:
	y_column = int(parse_result.y_column)
except:
	print(colorama.Back.RED + colorama.Style.BRIGHT + "PLOT ERROR: Invalid input parameter " +parse_result.y_column+ " for the column of y-values (integer conversion failed), exit."+ colorama.Style.NORMAL + colorama.Back.RESET)
	sys.exit(10)
flag_display_in_one_figure = parse_result.flag_display_in_one_figure	

# Wildcard expansion for the input file list:
file_list = []
for item in parse_result.input_file.split(","):
	file_list.extend(glob.glob(item))
if not file_list:
	print(colorama.Back.RED + colorama.Style.BRIGHT + "PLOT ERROR: Input file(s) " + file_list[0] + " cannot be found, nothing to do."+ colorama.Style.NORMAL + colorama.Back.RESET)
	sys.exit(10)
		
for file_cnt in range(0,len(file_list)):

	filename = file_list[file_cnt]
	
	# Read input file
	print("PLOT: Processing file: " + filename)
	print("  Reading data...")
	fin = rftools_bcf.ReadBCF(filename, True)
	if fin.flag_read_valid:
		print("  Finished reading data")
	else:
		print(colorama.Back.RED + colorama.Style.BRIGHT + "  ERROR: Failed reading file " + filename + ", exit."+ colorama.Style.NORMAL + colorama.Back.RESET)
		# Return code for error (failed reading input file):
		sys.exit(21)
	if fin.flag_empty_file or fin.number_of_segments < 1:
		print(colorama.Back.RED + colorama.Style.BRIGHT + "  ERROR: Empty file " + filename + ", exit."+ colorama.Style.NORMAL + colorama.Back.RESET)
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
		print(colorama.Back.YELLOW + colorama.Style.BRIGHT + "  Warning: Input file with more than one segment, only the first row of each segment will be plotted."+ colorama.Style.NORMAL + colorama.Back.RESET)
		
					
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
	
	if flag_display_in_one_figure:
		pltstyle = ''
	else:
		pltstyle = 'k'
	linestyle_list = parse_result.linestyle.split(',')
	if file_cnt < len(linestyle_list):
		linestyle = linestyle_list[file_cnt]
	else:
		linstyle = '0'
	if linestyle == '0':
		pltstyle += '.'
	elif linestyle == '1':
		pltstyle += '-'
	elif linestyle == '2':
		pltstyle += '--'
	elif linestyle == '3':
		pltstyle += ':'
	elif linestyle == '4':
		pltstyle += '-.'
	else:
		pltstyle += '.'
	markerstyle_list = parse_result.markerstyle.split(',')
	if file_cnt < len(markerstyle_list):
		markerstyle = markerstyle_list[file_cnt]
	else:
		markerstyle = '0'
	if markerstyle == '1':
		pltstyle += 'o'
	elif markerstyle == '2':
		pltstyle += '*'
	elif markerstyle == '3':
		pltstyle += 's'
	elif markerstyle == '4':
		pltstyle += 'v'
	elif markerstyle == '5':
		pltstyle += '^'
		
		
	x_column = x_column_list[0]
					
	if fin.number_of_segments > 1:
		x = np.ndarray(fin.number_of_segments)
		y = np.ndarray(fin.number_of_segments)
		for segment_cnt in range(0,fin.number_of_segments):
			x[segment_cnt] = fin.return_data(segment_cnt, x_column-1)[0] #+ fin.segment_times_in_100ns[segment_cnt]/1e7
			y[segment_cnt] = fin.return_data(segment_cnt, y_column-1)[0]
	else:
		x = fin.return_data(0, x_column-1)
		y = fin.return_data(0, y_column-1)	

	if not flag_display_in_one_figure or file_cnt == 0:
		if x_column > 0:
			print("  Segment time of first segment: " + str(fin.segment_times_in_100ns[0]/1e7) + " seconds.")
			if fin.number_of_segments > 1:
				print("  Segment time of last segment: " + str(fin.segment_times_in_100ns[-1]/1e7) + " seconds.")
			if parse_result.SI:
				x_factor = 1
				x_column_string = fin.column_information[x_column-1][3][:]
			else:
				x_factor, x_column_string = rftools_misc.auto_unit_conversion(fin.column_information[x_column-1][1], fin.column_information[x_column-1][3][:], np.max(np.abs(x[np.isfinite(x)])), parse_result.use_degree)
		else:
			x_factor = 1
			x_column_string = 'Index'
		
		if parse_result.SI:
			y_factor = 1
			y_column_string = fin.column_information[y_column-1][3][:]
		else:
			y_factor, y_column_string = rftools_misc.auto_unit_conversion(fin.column_information[y_column-1][1], fin.column_information[y_column-1][3][:], np.max(np.abs(y[np.isfinite(y)])), parse_result.use_degree)
	
	if not flag_display_in_one_figure or file_cnt == 0:
		fig = plt.figure()
	if x_column > 0:
		plt.plot(x_factor*x, y_factor*y, pltstyle)
	else:
		plt.plot(y_factor*y, pltstyle)
	if not flag_display_in_one_figure or file_cnt == 0:
		plt.ylabel(y_column_string, fontsize=14, color='black')
		plt.xlabel(x_column_string, fontsize=14, color='black')
		plt.autoscale(enable=True, axis='x', tight=False)


# Success:
plt.show()
print(colorama.Back.GREEN + colorama.Style.BRIGHT + "PLOT: Done." + colorama.Style.NORMAL + colorama.Back.BLACK)
sys.exit(0)

## @package RFTOOLS_CSV
# Python package with routines for RF data analysis.
#
# GSI-PBRF (D. Lens), 2016
version_string = 'Rev. 0.2.9, 03.08.2017'

# History
# Rev. 0.2.9: Removed bug in ReadCSV (.type was not always initialized)

import os, sys
from struct import unpack
from struct import pack
import numpy as np
#import matplotlib
#import matplotlib.pyplot as plt
import time
from math import ceil
import rftools_misc

## Class for reading comma seperated value (.csv) files.
# The definition of the file format can be found in the following document:
# H. Klingbeil, B. Zipfel: Data Analysis File Formats for RF Applications, GSI, rev. 0.80, 2011.
# (c)Dieter Lens (GSI, 2015)
class ReadCSV:
	# To Be Done:
	# - Check whether any number and combination of CR and LF works as new-line command

   	## Constructor by reading from a file
	#  @param self The object pointer.
	#  @param filename The name of the file to read
	#  @param number_of_header_list_to_ignore The number of header lines to be ignored (only needed for CSV files that are not in the specified CSV file format.
	def __init__(self,filename,number_of_header_list_to_ignore=0):
		self.filename = filename
		self.flag_read_valid = False # Set to True after successfully reading a CSV file
		self.number_of_header_list_to_ignore = number_of_header_list_to_ignore
		self.flag_file_opened = False
		self.flag_invalid_lines_detected = False
		self.columns = np.nan
		self.rows = np.nan
		self.read()

	def open(self):
		try:
			self.fin = open(self.filename,"r")
		except:
			print("ERROR: file " + self.filename + " could not be opened.")
			return -1
		self.flag_file_opened = True
		return 0

	def close(self):
		self.fin.close()
		self.flag_file_opened = False

	## Read a CSV file. All data/sample values are loaded into memory.
	#  @param self The object pointer
	def read(self):
	# Important guidelines (cf. the file format definition):
	# - Interpret any number and combination of CR and LF (0x0D and 0x0A, \r and \n in python) as one new-line command (this still has to be checked!)
	# - Ignore/remove empty lines
	# - Allowed delimiters: Comma (0x2C), Semicolon, Tab (\t in python)
	# - Remove leading and trailing spaces of an entry (python: string.strip())
		if not self.flag_file_opened:
			self.open()
		if not self.flag_file_opened:
			print("ERROR (ReadCSV.read()): file " + self.filename + " could not be opened.")
			return -1

		# Read content:
		content = self.fin.read()
		self.close()

		# Replace all semicolons and tabs by commas
		content = content.replace(";",",").replace("\t",",")
		lines = content.splitlines()
		if not lines:
			self.identifier = 'Basic CSV'
			self.x = np.ndarray((0,0))
			self.flag_read_valid = True
			self.time_stamp = ''
			return 1

		# First line: split with comma as delimiter:
		parts = lines[0].split(",",2)
		self.first_line = parts
		if parts == ['']:
			return -1 # invalid file
		self.identifier = parts[0].strip()
		if self.identifier in ['Ramp File', 'Time Function File', 'Column File', '2D File']:
			# Interpret keys: get rows, columns, time_stamp, and grouping
			if len(self.first_line) >= 2:
				self.columns = rftools_misc.get_key_value(self.first_line[1],'columns','int')
				self.rows = rftools_misc.get_key_value(self.first_line[1],'rows','int')
				self.grouping = rftools_misc.get_key_value(self.first_line[1],'grouping','string')
				self.time_stamp = rftools_misc.get_key_value(self.first_line[1],'time_stamp','string')
				self.device = rftools_misc.get_key_value(self.first_line[1],'device','string')
				self.user_name = rftools_misc.get_key_value(self.first_line[1],'user_name','string')
				self.unit = rftools_misc.get_key_value(self.first_line[1],'unit','int')
				self.segment_time = rftools_misc.get_key_value(self.first_line[1],'segment_time','float')
				self.segment_number = rftools_misc.get_key_value(self.first_line[1],'segment_number','int')
			if np.isnan(self.columns):
				self.columns = -1
			if np.isnan(self.rows):
				self.rows = -1

		# This might be a plain CSV file, try to read plain data:
		else:
			self.identifier = 'Basic CSV'
			self.time_stamp = ''
			self.x = []
			for cnt in range(self.number_of_header_list_to_ignore, len(lines)):
				parts = lines[cnt].split(",")
				if len(parts) == 1 and parts[0].strip() == '':
					continue # empty line
				try:
					templist = [float(x) for x in parts]
				except:
					templist = []
				if templist:
					if len(self.x) > 0 and not len(templist) == len(self.x[0]):
						self.flag_invalid_lines_detected
					else:
						self.x.append(templist)
				else:
					self.flag_invalid_lines_detected = True
			if self.x:
				try:
					self.x = np.array(self.x)
				except BaseException as exc:
					print(exc)
					print('ERROR (ReadCSV.read()): Reading file as plain CSV with ' +str(self.number_of_header_list_to_ignore)+ ' header lines to ignore failed.')
					return -1
				if len(self.x.shape) == 2:
					self.rows = self.x.shape[0]
					self.columns = self.x.shape[1]
			else:
				self.rows = 0
				self.columns = 0
			self.flag_read_valid = True
			return 0


		# The following content depends on the type of the CSV file:
		# Ramp File:
		if self.identifier in ['Ramp File', 'Time Function File']:
			# Read type of the ramp variable:
			self.column_types = [6, 0]
			self.column_units = [6, 0]
			if len(self.first_line) > 1:
				type = rftools_misc.get_key_value(self.first_line[1],'type','int')
				unit = rftools_misc.get_key_value(self.first_line[1],'unit','int')
				if not type == '':
					self.column_types = [6, type]
				if not unit == '':
					self.column_units = [6, unit]
			if len(lines) >= 2: # Second line:
				self.column_comments = lines[1].split(",")
			else:
				self.column_comments = ''
			# Further lines contain data:
			self.x = []
			for cnt in range(2, len(lines)):
				parts = lines[cnt].split(",")
				if not len(parts) == 2:
					continue # Skip empty or invalid line
					self.flag_invalid_lines_detected = True
				#if len(parts) < 2:
				#	print(len(parts))
				#	print('ERROR (ReadCSV.read()): wrong number of columns = ' + str(len(parts)) + ' in line ' + str(cnt) + ' detected (must be at least 2).')
				#	return -1
				try:
					self.x.append([float(parts[0]), float(parts[1])])
				except:
					print('ERROR (ReadCSV.read()): invalid format or character in line ' + str(cnt) + ' detected.')
					return -1
			self.x = np.row_stack(self.x)
			if self.columns == -1:
				self.columns = self.x.shape[1]
			# Check number of columns:
			if not self.columns in [-1, 2]:
				print('ERROR (ReadCSV.read()): ramp file must have exactly 2 columns.')
				return -1
			if self.rows == -1:
				self.rows = self.x.shape[0]
			if self.rows != len(self.x):
				print('ERROR (ReadCSV.read()): key value of rows does not match the number of data rows.')
				return -1
			self.flag_read_valid = True
			return 0

		# Column file:
		elif self.identifier == 'Column File':
			# Further lines:
			self.x = []
			if len(lines) >= 4:
				# Second line: type of variable for each column:
				try:
					self.column_types = [int(x) for x in lines[1].split(",")]
				except:
					print('ERROR (ReadCSV.read()): invalid character or format in line 2 detected.')
					return -1
				if self.columns == -1:
					self.columns = len(self.column_types)
				# Third line: units
				try:
					self.column_units = [int(x) for x in lines[2].split(",")]
				except:
					print('ERROR (ReadCSV.read()): invalid character or format in line 3 detected.')
					return -1
				if len(self.column_types) != len(self.column_units):
					return -1
				# Fourth line: comments for each column
				self.column_comments = lines[3].split(",")
				total_number_of_columns = self.columns
				for k in range(len(self.column_comments),total_number_of_columns): # guarantee that there are not less comments than columns
					self.column_comments.append('')
				# Further lines contain data:
				x = []
				for cnt in range(4, len(lines)):
					parts = lines[cnt].split(",")
					if len(parts) == 1 and parts[0].strip() == '':
						continue # empty line
					if len(parts) != total_number_of_columns:
						print('ERROR (ReadCSV.read()): wrong number of columns = ' + str(len(parts)) + ' in line ' + str(cnt) + ' detected.')
						return -1
					try:
						x.append([float(x) for x in parts])
					except:
						print('ERROR (ReadCSV.read()): invalid character or format in line ' + str(cnt) + ' detected.')
						return -1
				self.x = np.array(x)
				if self.rows == -1:
					self.rows = len(self.x)
			self.flag_read_valid = True
			return 0

		# 2D File:
		elif self.identifier == '2D File':
			if len(lines) >= 5:
				try:
					self.column_types = [int(x) for x in lines[1].split(",")]
				except:
					print('ERROR (ReadCSV.read()): invalid character or format in line 2 detected.')
					return -1
				if len(self.column_types) != 3:
					print('ERROR (ReadCSV.read()): in line 2, ' + str(len(self.column_types)) + ' type specifiers are given (must be 3).')
					return -1
				try:
					self.column_units = [int(x) for x in lines[2].split(",")]
				except:
					print('ERROR (ReadCSV.read()): invalid character or format in line 3 detected.')
					return -1
				if len(self.column_units) != 3:
					print('ERROR (ReadCSV.read()): in line 3, ' + str(len(self.column_types)) + ' unit specifiers are given (must be 3).')
					return -1
				self.column_comments = lines[3].split(",")
				for k in range(len(self.column_comments),3): # guarantee that there are not less comments than columns
					self.column_comments.append('')
				# Read Table content
				parts = lines[4].split(",")
				if parts[0] != 'Table':
					print("ERROR (ReadCSV.read()): format error in line 5: string 'Table' is not detected.")
					return -1
				self.x = []
				self.y = []
				self.z = []
				try:
					self.y = [float(x) for x in parts[1::] ]
					for cnt in range(5, len(lines)):
						parts = lines[cnt].split(",")
						if len(parts) == 1 and parts[0].strip() == '':
							continue # empty line
						self.x.append(float(parts[0]))
						self.z.append([float(x) for x in parts[1::]])
					self.x = np.array(self.x)
					self.y = np.array(self.y)
					self.z = np.array(self.z)
				except:
					print("ERROR (ReadCSV.read()): format error in floating point data detected.")
					return -1
			self.flag_read_valid = True
			return 0

		else:
			print('ERROR (ReadCSV.read()): format of CSV file is unknown.')
			return -1

	## @var filename
	#  The name of the file that is connected to this class

## Class for writing comma seperated value (.csv) files.
# The definition of the file format can be found in the following document:
# H. Klingbeil, B. Zipfel: Data Analysis File Formats for RF Applications, GSI, rev. 0.80, 2011.
# (c)Dieter Lens (GSI, 2015)
class WriteCSV:
	# To Be Done:
	# - Check if the file exists before writing.
	# - Check written file in hex: are lines seperated by CR&LF (0x0D 0x0A)?

   	## Constructor by reading from a file
	#  @param self The object pointer.
	#  @param filename The name of the file to write
	def __init__(self,filename):
		self.filename = filename
		self.flag_file_opened = False

	def open(self):
		try:
			self.fout = open(self.filename,"w")
		except:
			print("ERROR: file " + self.filename + " could not be opened.")
			return -1
		self.flag_file_opened = True
		return 0

	def close(self):
		self.fout.close()
		self.flag_file_opened = False

	## Write a CSV file.
	#  @param self The object pointer
	#  @param type_list List with 3 integers that specify the type of x, y, and z
	#  @param unit_list List with 3 integers that specify the unit of x, y, and z
	#  @param xyz_comment_list List with 3 strings that comment the variables x, y, z
	#  @param x		Numpy array with floats that specify the x-axis
	#  @param y 	Numpy array with floats that specify the y-axis
	#  @param z		Numpy 2D array/matrix with e.g. calibration data (number of rows = lenght(x_list), number of columns = length(y_list))
	#  @param delimiter Delimiter symbol: Comma, Semicolon, Tab (\t)
	#  @param overwrite If this flag is True, an existing file is overwritten without warning. If it is False, an error is produces and nothing is written.
	def write_2D_file(self,type_list,unit_list,xyz_comment_list,x,y,z,delimiter=',',overwrite=True):
		# First check the input parameters:
		if len(type_list) != 3 or len(unit_list) !=3 or len(xyz_comment_list) !=3:
			print('ERROR (WriteCSV.write_2D_file()): type list, unit list, and comment list must have 3 elements (strings) each.')
			return -1
		z_shape = z.shape
		if len(z_shape) == 2:
			rows, columns = z_shape[0], z_shape[1]
		if len(z_shape) == 1:
			rows, columns = z_shape[0], 1
		if rows != len(x) or columns != len(y):
			print('ERROR (WriteCSV.write_2D_file()): dimensions of x, y, z do not match.')
			return -1
		if overwrite == False:
			try:
				with open(self.filename,"r") as fin:
					pass
			except:
				print('ERROR (WriteCSV.write_2D_file()): file already exists, nothing is written.')
				return -1

		self.open()
		if not self.flag_file_opened:
			print("ERROR: file " + self.filename + " could not be opened.")
			return -1

		self.fout.write('2D File, columns=' + str(columns) + ' rows='+str(rows) + '\n')
		self.fout.write(str(type_list[0]) + delimiter + ' ' + str(type_list[1]) + delimiter + ' ' + str(type_list[2]) + '\n')
		self.fout.write(str(unit_list[0]) + delimiter + ' ' + str(unit_list[1]) + delimiter + ' ' + str(unit_list[2]) + '\n')
		self.fout.write(xyz_comment_list[0] + delimiter + ' ' + xyz_comment_list[1] + delimiter + ' ' + xyz_comment_list[2] + '\n')
		line = 'Table'
		for cnt in range(0,columns):
			line += delimiter + ' ' + str(y[cnt])
		self.fout.write(line + '\n')
		for row_cnt in range(0,rows):
			line = str(x[row_cnt])
			if columns > 1:
				for col_cnt in range(0,columns):
					line += delimiter + ' ' + str(z[row_cnt,col_cnt])
			else:
				line += delimiter + ' ' + str(z[row_cnt])
			self.fout.write(line + '\n')

		self.close()
		return 0

	## Write a CSV ramp file.
	#  @param self The object pointer
	#  @param ramp_type Integer that specifies the ramp type (0: unspecified, 1: B field, 2: synchronous phase, 3: RF amplitude, 4: RF frequency, 5: relativistic gamma, 6: time, 7: revolution frequency, 8: RF phase, 50: beam current, 103: voltage, 104: frequency, 105: harmonic number, 106: impedance, 107: phase, 108: current, 109: temperature, 200: time stamp)
	#  @param ramp_unit Integer that specifies the ramp unit (0: unspecified, 1: T, 2: rad, 3: V, 4: Hz, 5: dimensionless, 6: s, 50: C, 60: Ohm, 61: A, 62: a.u., 200: system ticks)
	#  @param y_comment_string String that comments the variables y
	#  @param t	List or Numpy array with floats that specify the t-axis
	#  @param y 	List or Numpy array with floats that specify the y-axis
	#  @param delimiter Delimiter symbol: Comma, Semicolon, Tab (\t)
	#  @param overwrite If this flag is True, an existing file is overwritten without warning. If it is False, an error is produces and nothing is written.
	def write_ramp_file(self,ramp_type,ramp_unit,y_comment_string,t,y,delimiter=',',overwrite=True):
		# Check input parameters
		if not(len(t) == len(y)):
			print('ERROR (WriteCSV.write_ramp_file()): dimensions of t and y do not match.')
			return -1
		if overwrite == False:
			try:
				with open(self.filename,"r") as fin:
					pass
			except:
				print('ERROR (WriteCSV.write_ramp_file()): file already exists, nothing is written.')
				return -1

		self.open()
		if not self.flag_file_opened:
			print("ERROR: file " + self.filename + " could not be opened.")
			return -1

		self.fout.write('Ramp File, type=' + str(ramp_type) + ' unit='+str(ramp_unit) + '\n')
		self.fout.write('t/s, ' + y_comment_string + '\n')
		for cnt in range(0,len(t)):
			self.fout.write(str(t[cnt]) + ', ' + str(y[cnt]) + '\n')

		self.close()
		return 0


	## Write a CSV column file.
	# Usage example:
	# write_column_file([6, 103], [6, 3], np.ndarray([[0,1],[1,0.5],[2,0]]))
	#  @param self The object pointer
	#  @param type_list List with N integers that specify the type of each column.
	#  @param unit_list List with N integers that specify the unit of each column.
	#  @param comment_list List with N strings that comment the columns
	#  @param x	Numpy array or 2D-array with floats that specify the values, x[k,m] is the kth value of the mth column, i.e. x[:,0] are the values of the first column.
	#  @param delimiter Delimiter symbol: Comma, Semicolon, Tab (\t)
	#  @param further_entries List of description strings that are appended to the first line of the file
	#  @param overwrite If this flag is True, an existing file is overwritten without warning. If it is False, an error is produces and nothing is written.
	def write_column_file(self,type_list,unit_list,comment_list,x,delimiter=', ',further_entries=[],overwrite=True,time_stamp='',grouping='none',device='',user_name=''):
		# First check the input parameters:
		N_columns = len(type_list)
		if len(unit_list) != N_columns or len(comment_list) != N_columns:
			print('ERROR (WriteCSV.write_column_file()): type list, unit list, and comment list must have identical number of elements (strings) each.')
			return -1
		x = np.array(x)
		x_shape = x.shape
		if len(x_shape) == 2:
			rows, columns = x_shape[0], x_shape[1]
		if len(x_shape) == 1:
			if len(comment_list) == 1:
				rows, columns = x_shape[0], 1
			else:
				rows, columns = 1, x_shape[0]
		if columns != N_columns:
			print('ERROR (WriteCSV.write_column_file()): dimensions of x do not match.')
			return -1
		if overwrite == False:
			try:
				with open(self.filename,"r") as fin:
					pass
			except:
				print('ERROR (WriteCSV.write_column_file()): file already exists, nothing is written.')
				return -1

		self.open()
		if not self.flag_file_opened:
			print("ERROR: file " + self.filename + " could not be opened.")
			return -1

		line_1 = 'Column File, columns=' + str(columns) + ' rows='+str(rows)
		if time_stamp:
			line_1 += ' time_stamp=' + time_stamp
		if grouping:
			line_1 += ' grouping=' + grouping
		if device:
			line_1 += ' device=' + device
		if user_name:
			line_1 += ' user_name=' + user_name
		if further_entries:
			for entry in further_entries:
				line_1 += ' ' + entry
		self.fout.write(line_1 + '\n')
		line_2, line_3, line_4 = '', '', ''
		for cnt in range(0,columns-1):
			line_2 += str(type_list[cnt]) + delimiter
			line_3 += str(unit_list[cnt]) + delimiter
			line_4 += comment_list[cnt] + delimiter
		self.fout.write(line_2 + str(type_list[columns-1]) + '\n')
		self.fout.write(line_3 + str(unit_list[columns-1]) + '\n')
		self.fout.write(line_4 + comment_list[columns-1] + '\n')
		# Write data values
		if columns == 1:
			for cnt in range(0,rows):
				self.fout.write(str(x[cnt]) + '\n')
		elif rows == 1:
			line = ''
			if len(x.shape) == 1:
				for cnt in range(0,columns-1):
					line += str(x[cnt]) + delimiter
				self.fout.write(line + str(x[columns-1]) + '\n')
			else:
				for cnt in range(0,columns-1):
					line += str(x[0,cnt]) + delimiter
				self.fout.write(line + str(x[0,columns-1]) + '\n')
		else:
			for row_cnt in range(0,rows):
				line = ''
				for col_cnt in range(0,columns-1):
					line += str(x[row_cnt,col_cnt]) + delimiter
				self.fout.write(line + str(x[row_cnt,columns-1]) + '\n')

		self.close()
		return 0


	## Write a plain CSV file.
	#  @param self The object pointer
	#  @param x	Numpy array or 2D-array with floats that specify the values, x[k,m] is the kth value of the mth column, i.e. x[:,0] are the values of the first column.
	#  @param overwrite If this flag is True, an existing file is overwritten without warning. If it is False, an error is produces and nothing is written.
	def write_plain_file(self,x,delimiter=',',overwrite=True):
		# First check the input parameters:
		x = np.array(x)
		x_shape = x.shape
		if len(x_shape) == 2:
			rows, columns = x_shape[0], x_shape[1]
		if len(x_shape) == 1:
			#if len(comment_list) == 1:
				rows, columns = x_shape[0], 1
			#else:
			#	rows, columns = 1, x_shape[0]
		if overwrite == False:
			try:
				with open(self.filename,"r") as fin:
					pass
			except:
				print('ERROR (WriteCSV.write_plain_file()): file already exists, nothing is written.')
				return -1

		self.open()
		if not self.flag_file_opened:
			print("ERROR: file " + self.filename + " could not be opened.")
			return -1

		# Write data values
		if columns == 1:
			for cnt in range(0,rows):
				self.fout.write(str(x[cnt]) + '\n')
		elif rows == 1:
			line = ''
			for cnt in range(0,columns-1):
				line += str(x[cnt]) + delimiter
			self.fout.write(line + str(x[columns-1]) + '\n')
		else:
			for row_cnt in range(0,rows):
				line = ''
				for col_cnt in range(0,columns-1):
					line += str(x[row_cnt,col_cnt]) + delimiter
				self.fout.write(line + str(x[row_cnt,columns-1]) + '\n')

		self.close()
		return 0

	## @var filename
	#  The name of the file that is connected to this class

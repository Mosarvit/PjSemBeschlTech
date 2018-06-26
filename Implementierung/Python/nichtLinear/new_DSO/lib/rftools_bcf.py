#!/usr/bin/python3
## @package RFTOOLS_BCF
# Python package with routines for RF data analysis.
# GSI, RRF, D. Lens (2016-2018)
version_string = '0.2.13, 24.01.2018'

## History
# Rev 0.2.13:
# - Removed matplotlib from the imported libraries
# Rev. 0.2.12:
# - Endianness fixed to little endianness

import os, sys
from struct import unpack
from struct import pack
import numpy as np
import time, datetime
from math import ceil

## Class for reading Binary Column Files (.bcf) files.
# The definition of the Binary Column Files can be found in the following document:
# H. Klingbeil, B. Zipfel: Data Analysis File Formats for RF Applications, GSI, rev. 0.90, 2016.
# (c)Dieter Lens (GSI, 2016-2017)
class ReadBCF:

   	## Constructor by reading from a file
	#  @param self The object pointer.
	#  @param filename The name of the file to read
	#  @param flag_read_all If this flag is True (this is the default), the complete data of the file is loaded into memory.
	def __init__(self,filename,flag_read_all=True):
		self.filename = filename
		self.x_full = []
		self.x_part = []
		self.flag_read_valid = False
		self.flag_file_opened = False
		self.flag_header_read = False
		self.flag_empty_file = True
		self.endianness_string = '<'	# Little endian
		self.read_header()
		self.flag_read_all = flag_read_all
		if flag_read_all:
			self.read_complete_data()

	def open(self):
		try:
			self.fin = open(self.filename,"rb")
		except:
			print("ERROR: file " + self.filename + " could not be opened.")
			return -1
		self.flag_file_opened = True
		return 0

	def close(self):
		self.fin.close()
		self.flag_file_opened = False

	## Read options from a BCF file. The data/sample values are not loaded into memory.
	#  @param self The object pointer
	def read_header(self):
		if self.flag_header_read:
			return 0
		if not self.flag_file_opened:
			self.open()
		if not self.flag_file_opened:
			print("ERROR: file " + self.filename + " could not be opened.")
			return -1

		self.fin.seek(0,0)
		self.magic_numbers = self.fin.read(32).decode("utf-8")  # magic numbers including file format version

		# read header
		temp = self.fin.read(4)
		if (temp == b'HEAD') == False:
			print('Error (rftools.ReadBCF()): BCF file ' + self.filename + ' seems corrupted.')
			print("Expected the string 'HEAD', but found: " + str(temp))
			return -1
		n_bytes = unpack(self.endianness_string+'I',self.fin.read(4))[0]
		self.time_stamp = unpack(self.endianness_string+'d',self.fin.read(8))[0]             # 100 ns steps since epoch
		self.time_stamp_string = datetime.datetime.fromtimestamp(self.time_stamp/1e7).strftime('%Y-%m-%d %H:%M:%S.%f')[0:-3]
		self.number_of_segments = unpack(self.endianness_string+'I',self.fin.read(4))[0]
		self.number_of_columns = unpack(self.endianness_string+'I',self.fin.read(4))[0]
		self.fin.read(256) # 256 bytes of zeros (reserved)
		self.header_description_string = self.fin.read(n_bytes-8-4-4-256).decode("utf-8")

		# read column information:
		self.column_information = []
		for col_cnt in range(0,self.number_of_columns):
			temp = self.fin.read(4)
			if (temp == b'COL ') == False:
				print('Error (rftools.ReadBCF()): BCF file ' + self.filename + ' seems corrupted.')
				print("Expected the string 'COL ', but found: " + str(temp))
				return -1
			n_bytes = unpack(self.endianness_string+'I',self.fin.read(4))[0]
			quantity_type = unpack(self.endianness_string+'I',self.fin.read(4))[0]
			unit = unpack(self.endianness_string+'I',self.fin.read(4))[0]
			representation = unpack(self.endianness_string+'I',self.fin.read(4))[0]
			self.fin.read(256) # reserved bytes
			description_string = self.fin.read(n_bytes-3*4-256).decode("utf-8")[0:-1]  # [0:-1] removes the trailing NULL character
			self.column_information.append([quantity_type, unit, representation, description_string])
			if (representation != 0) and (representation != 1):
				print('Warning (ReadBCF.read_header()): unknown data type (representation): ' + str(representation))

		# collect the structure of one column and make a numpy.dtype of it:
		self.record_dtype = []
		for col_cnt in range(0,self.number_of_columns):
			if self.column_information[col_cnt][2] == 0: # float representation
				self.record_dtype.append( ('c'+str(col_cnt), 'f') )
			elif self.column_information[col_cnt][2] == 1: # double representation
				self.record_dtype.append( ('c'+str(col_cnt), 'd') )
			else:
				print("ERROR (rftools_bcf.ReadBCF.read_complete_data()): unkown column data type " + self.column_information[col_cnt][2])
				return -1

		self.file_position_segments = np.ndarray((self.number_of_segments), dtype=np.int)
		self.segment_times_in_100ns = np.ndarray((self.number_of_segments))
		self.segment_number_of_rows = np.ndarray((self.number_of_segments), dtype=np.int)

		# read the headers of the segment chunks:
		for seg_cnt in range(0,self.number_of_segments):

			# save the file position where the segments begin:
			self.file_position_segments[seg_cnt] = self.fin.tell()
			temp = self.fin.read(4)
			if (temp == b'SEGM') == False:
				print('Error (rftools.ReadBCF()): BCF file ' + self.filename + ' seems corrupted.')
				print("Expected the string 'SEGM', but found: " + str(temp))
				return -1
			n_bytes = unpack(self.endianness_string+'I',self.fin.read(4))[0]
			# read segment time and number of rows
			self.segment_times_in_100ns[seg_cnt] = unpack(self.endianness_string+'d',self.fin.read(8))[0]
			self.segment_number_of_rows[seg_cnt] = unpack(self.endianness_string+'I',self.fin.read(4))[0]
			self.fin.seek(n_bytes-8-4, 1) # skip content

		# read the keys chunk:
		temp = self.fin.read(4)
		if (temp == b'KEYS') == False:
			print("Warning (rftools.ReadBCF()): BCF file ' + self.filename + ' seems corrupted. Expected the string 'KEYS', but found: " + str(temp) + ".")
			self.keys_string = ''
		else:
			n_bytes = unpack(self.endianness_string+'I',self.fin.read(4))[0]
			self.keys_string = self.fin.read(n_bytes-1).decode("utf-8")
		self.flag_read_valid = True
		self.flag_header_read = True

		if self.number_of_segments == 0 or self.number_of_columns == 0 or len(self.segment_number_of_rows)==0:
			self.flag_empty_file = True
		else:
			self.flag_empty_file = False
		return 0


	## Read a data portion from the BCF file into memory
	# @param self The object pointer
	# @param segment_nr Defines the segment from which data is read. The first segment has index 0.
	# @param column_nr Defines the column from which data is read. The first column has index 0.
	# @param start_row Defines the first data sample (row) to be read. The first row has index 0.
	# @param number_of_samples The number of samples (rows) that is to be read (for stepsize = 1). For the default value -1, all available rows following the starting index are read. For stepsize > 1, the number of samples read will be smaller accordingly.
	# @param stepsize Stepsize of the sample index. Default value is 1. Example: for stepsize = 10, only every 10th sample (row) will be read.
	def read_data_portion(self,segment_nr,column_nr,start_row=0,number_of_samples=-1,stepsize=1):

		if self.flag_empty_file:
			print('Warning (ReadBCF.read_data_portion()): file is empty.')
			return -1

		# check input parameters:
		if start_row < 0:
			start_row = 0
		if (segment_nr < 0) or (segment_nr > self.number_of_segments-1):
			print('Error (ReadBCF.read_data_portion()): chosen segment does not exist for this file')
			return -1
		stepsize = max(int(stepsize), 1)

		self.fin.seek(self.file_position_segments[segment_nr],0) # go to the chosen segment:
		self.fin.read(256 + 4 + 4 + 8 + 4) # skip header

		# determine number of rows to be read
		number_of_rows = self.segment_number_of_rows[segment_nr] - start_row # all available rows
		if not (number_of_samples == -1):
			number_of_rows = min(number_of_samples, number_of_rows)
		number_of_rows = int( number_of_rows / stepsize )

		self.x_part = np.ndarray(number_of_rows)

		# skip unwanted rows:
		for skip_cnt in range(0, start_row):
			np.fromfile(self.fin, dtype=np.dtype(self.record_dtype), count=1) # read one row

		# read the data column by column:
		for row_cnt in range(0,number_of_rows):
			row_data = np.fromfile(self.fin, dtype=np.dtype(self.record_dtype), count=1) # read one row
			self.x_part[row_cnt] = row_data['c'+str(column_nr)]
			# skip stepsize-1 rows:
			for skip_cnt in range(0,stepsize-1):
				np.fromfile(self.fin, dtype=np.dtype(self.record_dtype), count=1)

		return 0


	## Read the complete data into memory
	# @param self The object pointer
	def read_complete_data(self):

		if self.flag_empty_file:
			print('Warning (ReadBCF.read_complete_data()): file is empty.')
			return -1

		# go to the segment position:
		self.fin.seek(self.file_position_segments[0],0)

		# the data will be saved in a list that contains Numpy arrays:
		self.x_full = []

		# iterate through all segments:
		Nc = self.number_of_columns
		for seg_cnt in range(0, self.number_of_segments):
			self.fin.read(4 + 4 + 8 + 4 + 256) # skip the segment header
			self.x_full.append( np.fromfile(self.fin, dtype=np.dtype(self.record_dtype), count=self.segment_number_of_rows[seg_cnt]) )

		# success, return 0
		return 0


	## Return the data of a certain segment and column as a Numpy array
	# @param self The object pointer
	# @param segment_nr Defines the segment from which data is read. The first segment has index 0.
	# @param column_nr Defines the column from which data is read. The first column has index 0.
	# @param start_row Defines the first data sample (row) to be read. The first row has index 0.
	# @param end_row Defines the last data sample (row) to be read. The first row has index 0.
	# @param step Defines the stepsize of the row selection.
	def return_data(self, segment_nr, column_nr, start_row=0, end_row=-1, step=1):

		if self.flag_empty_file:
			print('Warning (ReadBCF.return_data()): file is empty.')
			return []

		if segment_nr < 0 or segment_nr > self.number_of_segments:
			print("ERROR (rftools_bcf.readBCF): invalid segment number: " + str(segment_nr))
			return []
		if column_nr < 0 or column_nr > self.number_of_columns:
			print("ERROR (rftools_bcf.readBCF): invalid column number: " + str(column_nr))
			return []

		# if no data has been read yet, just read the specified segment:
		if not self.x_full:
			if end_row == -1:
				self.read_data_portion(segment_nr, column_nr, start_row, -1, step)
			else:
				self.read_data_portion(segment_nr, column_nr, start_row, end_row-start_row+1, step)
			return self.x_part
		else:
			if end_row == -1:
				return self.x_full[segment_nr]['c'+str(column_nr)][start_row::step]
			else:
				return self.x_full[segment_nr]['c'+str(column_nr)][start_row:end_row+1:step]


	## @var filename
	#  The name of the file that is connected to this class
	## @var x
	#  Sample values of data read from the BCF file


## Class for writing Binary Column Files (.bcf) files.
# The definition of the Binary Column Files can be found in the following document:
# H. Klingbeil, B. Zipfel: Data Analysis File Formats for RF Applications, GSI, rev. 0.80, 2011.
# (c)Dieter Lens (GSI, 2015)
class WriteBCF:

   	## Constructor
	# Usage example for a file with 1 segment and 2 columns:
	# WriteBCF('file.bcf', 0, 'Created by XY', 'device="PC"', [(6,6,1,'t/s'),(3,3,1,'y/v')], 1)
	# After this, the functions 'write_segment' and 'write_keys'
	#  @param self The object pointer.
	#  @param filename The name of the file that is to be written.
	#  @param Time stamp (double) for first segment as defined by [Klingbeil and Zipfel, 2011] (100-nanoseconds-steps since epoche, e.g. time.time()*1e7))
	#  @param header_description_string Description string for header of BCF file, including terminating zero.
	#  @param keys_string String with arbitrary number of keys, including terminating zero.
	#  @param column_information Array of lists including the column information. The lists have the form (quantity_type, unit, representation, description_string). As representation, the following values are valid: 0 (32-bit float), 1 (64-bit double)
	#  @param number_of_segments Number of segments of the BCF. If the parameter is not defined, the header of the BCF is updated (with regard to the position that stores the number of segments) each time a new segment is written to it.
	def __init__(self,filename,time_stamp,header_description_string='',keys_string='',column_information=[(6,6,1,'t/s'),(3,3,1,'y/V')],number_of_segments=0):
		self.filename = filename
		self.time_stamp = time_stamp
		self.warning_flag = False # In case of invalid parameters, this flag is set to prevent corrupted file output
		self.endianness_string = '<'	# Little endian
		self.number_of_columns = len(column_information)
		if number_of_segments < 1:
			self.number_of_segments = 0
			self.flag_update_number_of_segments = True
		else:
			self.number_of_segments = number_of_segments
			self.flag_update_number_of_segments = False
		if self.number_of_columns < 1:
			self.warning_flag = True
		for col_cnt in range(0,len(column_information)):
			if len(column_information[col_cnt]) != 4:
				self.warning_flag = True
			if not((column_information[col_cnt][2]==0) or (column_information[col_cnt][2]==1)):
				self.warning_flag = True
		if self.warning_flag == True:
			print('Warning (WriteBCF.init()): invalid number of columns per segment!')
		# check if terminating zeros are present:
		if header_description_string[-1] != '\x00':
			header_description_string = header_description_string + '\x00'
		self.header_description_string = header_description_string
		infcopy = []
		for i, lc in enumerate(column_information):
			if lc[3][-1] != '\x00':
				temp = (lc[0],lc[1],lc[2],lc[3]+'\x00')
			else:
				temp = lc
			infcopy.append(temp)
		self.column_information = infcopy
		#if len(keys_string) == 0:
		#	self.keys_string = '\x00'
		#elif keys_string[-1] != '\x00':
		#	self.keys_string = keys_string + '\x00'
		#else:
		#	self.keys_string = keys_string
		self.keys_string = keys_string
		self.flag_file_opened = False
		# Write the header of the file:
		self.flag_header_written = False
		self.write_header()

	def open(self):
		try:
			self.fout = open(self.filename,"w+b")
		except:
			print("ERROR: file " + self.filename + " could not be opened.")
			return -1
		self.flag_file_opened = True
		return 0

	def close(self):
		self.fout.close()
		self.flag_file_opened = False

	## Write options to a BCF file.
	#  @param self The object pointer
	def write_header(self):
		if self.flag_header_written:
			return 0
		if self.warning_flag == True:
			print('Warning (WriteBCF.init()): invalid parameters, no output will be written!')
			return -1
		if not self.flag_file_opened:
			self.open()
		if not self.flag_file_opened:
			print("ERROR: file " + self.filename + " could not be opened.")
			return -1

		self.fout.write('BINARY_COLUMN_FILE_VERS_00.80\x00\x00\x00'.encode('utf-8'))	# magic numbers
		# write header
		self.fout.write(b'HEAD')
		n_bytes = 8+4+4+256+len(self.header_description_string)
		self.fout.write(pack(self.endianness_string+'I',n_bytes)) # number of bytes of header content
		# header content
		self.fout.write(pack(self.endianness_string+'d',self.time_stamp)) # time stamp; for current time stamp, use: self.fout.write(pack('d',time.time()*1e7))
		self.fout.write(pack(self.endianness_string+'I',self.number_of_segments)) # number of segments, may be equal to zero if the value is not specified in advance; this value will be updated for each new segment that is added (see function write_segment() of this class.
		self.fout.write(pack(self.endianness_string+'I',self.number_of_columns)) # number of columns per segment
		self.fout.write(bytearray([0 for x in range(0,256)])) # 256 bytes of zeros (reserved)
		self.fout.write((self.header_description_string).encode('utf-8'))
		# write column information:
		for col_cnt in range(0,self.number_of_columns):
			self.fout.write(b'COL ')
			# calculate number of bytes:
			n_bytes = 4*3+256+len(self.column_information[col_cnt][3])
			self.fout.write(pack(self.endianness_string+'I',n_bytes))
			self.fout.write(pack(self.endianness_string+'I',self.column_information[col_cnt][0])) # write quantity type, 32 bit unsigned
			self.fout.write(pack(self.endianness_string+'I',self.column_information[col_cnt][1])) # write unit, 32 bit unsigned
			self.fout.write(pack(self.endianness_string+'I',self.column_information[col_cnt][2])) # write representation, 32 bit unsigned
			self.fout.write(bytearray([0 for x in range(0,256)])) # 256 bytes of zeros (reserved)
			self.fout.write((self.column_information[col_cnt][3]).encode('utf-8')) # write description string including terminating zero

		# success
		self.flag_header_written = True
		return 0

	## Write options to a BCF file.
	#  @param self The object pointer
	#  @param relative_time_in_100ns Relative time (double in 100 ns steps) with respect to first segment/header time
	#  @param x    Numpy ndarray, array containing the segment data. The number of columns should be equal to self.number_of_columns.
	def write_segment(self,relative_time_in_100ns,x):
		if x.shape[1] != self.number_of_columns:
			print('Error (WriteBCF.write_segment()): shape of given data is incompatible with the given number of columns!')
			return -1
		number_of_rows = x.shape[0]

		# go to end of file:
		#self.fout.seek(0,2)
		self.fout.write(b'SEGM')
		# calculate number of bytes of content
		n_bytes = 8+4+256
		for col_cnt in range(0,self.number_of_columns):
			if self.column_information[col_cnt][2] == 0: # float representation
				n_bytes = n_bytes + 4*number_of_rows
			elif self.column_information[col_cnt][2] == 1: # double representation
				n_bytes = n_bytes + 8*number_of_rows
		self.fout.write(pack(self.endianness_string+'I',n_bytes)) # number of bytes of content
		# write segment header:
		self.fout.write(pack(self.endianness_string+'d',relative_time_in_100ns)) # relative time with respect to first segment
		self.fout.write(pack(self.endianness_string+'I',number_of_rows)) # number of rows in this segment
		self.fout.write(bytearray([0 for x in range(0,256)])) # 256 bytes of zeros (reserved)

		# write values:
		flag_all_have_equal_representation = True
		for col_cnt in range(1,self.number_of_columns):
			if not self.column_information[col_cnt][2] == self.column_information[0][2]:
				flag_all_have_equal_representation = False
				break
		if flag_all_have_equal_representation:
			if self.column_information[0][2] == 0: # float
				self.fout.write(x.astype('f').tostring())
			if self.column_information[0][2] == 1: # double
				self.fout.write(x.astype('d').tostring())
		else: # write the slow way
			for row_cnt in range(0,number_of_rows):
				for col_cnt in range(0,self.number_of_columns):
					if self.column_information[col_cnt][2] == 0: # float representation
						self.fout.write(pack(self.endianness_string+'f',x[row_cnt][col_cnt]))
					if self.column_information[col_cnt][2] == 1: # double representation
						self.fout.write(pack(self.endianness_string+'d',x[row_cnt][col_cnt]))
		
		# increase the segment counter in the header of the file:
		if self.flag_update_number_of_segments:
			self.fout.seek(48,0) # go to the position of the segment number
			number_of_segments = unpack(self.endianness_string+'I',self.fout.read(4))[0]
			self.fout.seek(48,0)
			self.fout.write(pack(self.endianness_string+'I',number_of_segments+1)) # increase number of segments by 1
			self.fout.seek(0,2)	# go to end of file

		# success
		return 0

	## Write key string to a BCF file.
	#  @param self The object pointer
	def write_keys(self):
		#self.fout.seek(0,2)
		self.fout.write(b'KEYS')
		n_bytes = len(self.keys_string)+1 # +1 for terminating zero
		self.fout.write(pack(self.endianness_string+'I',n_bytes)) # number of bytes of header content
		self.fout.write((self.keys_string+'\x00').encode('utf-8'))
		# Close the file:
		self.close()
		return 0


	## @var filename
	#  The name of the file that is connected to this class

#!/usr/bin/python3
## @package RFTOOLS_TRC
# Python package with routines for RF data analysis.
# 
revision_string = '0.6.2, 21.11.2016'

import os, sys
from struct import unpack
from struct import pack
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import time
from math import ceil

revision_string = '0.2.1, 10.10.2016'

## Class for reading waveform (trace, .trc) files created by LeCroy Oscilloscopes.
# Provides a data structure constructed by reading .trc files.
# Assuming the correct template is provided, this module generates a
# data structure holding the sampled data as well as the options, date,
# labels of the run.
# First version of the read function by Thibault Ferrand, Yun Ouedraogo (TEMF, TU Darmstadt, 2015)
# Modifications and extensions by Dieter Lens (GSI, 2015)
class ReadTRC:

   	## Constructor by reading from a file
	#  @param self The object pointer.
	#  @param filename The name of the file to read
	def __init__(self,filename):
		self.x = np.ndarray(0)
		self.y = np.ndarray(0)	
		self.filename = filename
		self.flag_read_valid = False
		self.flag_file_opened = False
		self.flag_header_read = False
		self.read_header()
		
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
    
	## Read data and options from a file
	#  @param self The object pointer.
	#  @param filename The name of the file to read
	def read_header(self):
		if self.flag_header_read:
			return 0
		if not self.flag_file_opened:
			self.open()
		if not self.flag_file_opened:
			print("ERROR: file " + self.filename + " could not be opened.")
			return -1
			
		data = []
		
		# Look for the beginning of the header
		a_wave_desc = self.fin.read(50).find(b'WAVEDESC',0,50)
		
		# Calculate the adresses of the fields in the header
		a_template_name = a_wave_desc + 16
		a_comm_type = a_wave_desc + 32
		a_comm_order = a_wave_desc + 34
		a_wave_descriptor = a_wave_desc + 36
		a_user_text = a_wave_desc + 40
		a_trigtime_array = a_wave_desc + 48
		a_wave_array = a_wave_desc + 60         # (Address of) total number of bytes of sample array (i.e. data)
		a_instrument_name = a_wave_desc + 76
		a_instrument_number = a_wave_desc + 92
		a_trace_label = a_wave_desc + 96
		a_wave_array_count = a_wave_desc + 116  # (Address of) total number of samples
		a_subarray_count = a_wave_desc + 144
		a_vertical_gain = a_wave_desc + 156
		a_vertical_offset = a_wave_desc + 160
		a_nominal_bits = a_wave_desc + 172
		a_horiz_interval = a_wave_desc + 176
		a_horiz_offset = a_wave_desc + 180
		a_vertunit = a_wave_desc + 196
		a_horunit = a_wave_desc + 244
		a_trigger_time = a_wave_desc + 296
		a_record_type = a_wave_desc + 316
		a_processing_done = a_wave_desc + 318
		a_timebase = a_wave_desc + 324
		a_vert_coupling = a_wave_desc + 326
		a_probe_att = a_wave_desc + 328
		a_fixed_vert_gain = a_wave_desc + 332
		a_bandwidth_limit = a_wave_desc + 334
		a_vertical_vernier = a_wave_desc + 336
		a_acq_vert_offset = a_wave_desc + 340
		a_wave_source = a_wave_desc + 344

		# Read the byte ordering from the header (little or big endian)
		self.fin.seek(a_comm_order)
		comm_order = unpack('h',self.fin.read(2))

		# Byte ordering string for the unpacking options
		if comm_order:
				bo = '<'
		else:
			bo = '>'
		self.bo = bo

		# Read and store the options, instrument name and date
		self.fin.seek(a_instrument_name)
		self.instrument_name = unpack(bo + '16s',self.fin.read(16))[0].decode("utf-8").rstrip('\0')
		self.fin.seek(a_instrument_number)
		self.instrument_number = unpack(bo + 'l',self.fin.read(4))
		self.fin.seek(a_trigger_time)
		secs,mins,hours,days,months,years, = unpack(bo + 'd4bh',self.fin.read(14))		
		#self.time_of_measurement = '{}.{}.{}, {}:{}:{}'.format(days, months,years, hours, mins, secs)
		self.time_of_measurement = "'{}-{:02d}-{:02d} {:02d}:{:02d}:{:06.3f}'".format(years, months, days, hours, mins, secs)

		tmp = ('channel 1', 'channel 2', 'channel 3', 'channel 4', 'unknown')
		self.fin.seek(a_wave_source)
		self.wave_source = tmp[unpack(bo + 'h',self.fin.read(2))[0]]

		tmp = ('DC_50_Ohms', 'ground','DC 1MOhm','ground','AC 1MOhm')
		self.fin.seek(a_vert_coupling)
		self.vert_coupling = tmp[unpack(bo + 'h',self.fin.read(2))[0]]

		tmp = ('off', 'on ')
		self.fin.seek(a_bandwidth_limit)
		self.bandwidth_limit = tmp[unpack(bo + 'h',self.fin.read(2))[0]]

		tmp = ( 'single_sweep',    'interleaved', 'histogram', 'graph', 'filter_coefficient', 'complex', 'extrema',  'sequence_obsolete', 'centered_RIS', 'peak_detect')
		self.fin.seek(a_record_type)
		self.record_type = tmp[unpack(bo + 'h',self.fin.read(2))[0]]

		tmp = ('no_processing', 'fir_filter', 'interpolated', 'sparsed', 'autoscaled', 'no_result', 'rolling', 'cumulative')
		self.fin.seek(a_processing_done)
		self.processing_done = tmp[unpack(bo + 'h',self.fin.read(2))[0]]

		# Reading and storing the vertical settings
		tmp = (1,2,5)
		self.fin.seek(a_fixed_vert_gain)
		fvg_str, = unpack(bo + 'h',self.fin.read(2))
		fixed_vertical_gain=tmp[fvg_str % 3] * 10 ** ((fvg_str // 3) - 6)

		self.fin.seek(a_probe_att)
		probe_att, = unpack(bo + 'f',self.fin.read(4))
		self.fin.seek(a_vertical_gain)
		self.vertical_gain, = unpack(bo + 'f',self.fin.read(4))
		self.fin.seek(a_vertical_offset)
		self.vertical_offset, = unpack(bo + 'f',self.fin.read(4))
		self.fin.seek(a_nominal_bits)
		self.nominal_bits, = unpack(bo + 'h',self.fin.read(2))
		
		self.gain_with_probe = str(fixed_vertical_gain*probe_att) + 'V/div'
		
		# Reading and storing the horizontal settings
		self.fin.seek(a_horiz_interval)
		horiz_interval, = unpack(bo + 'f',self.fin.read(4))
		self.fin.seek(a_horiz_offset)
		self.horiz_offset = unpack(bo + 'd',self.fin.read(8)) # trigger offset for the first sweep of the trigger
		self.fin.seek(a_fixed_vert_gain)
		tb_str, = unpack(bo + 'h',self.fin.read(2))
		
		tmp = (1,2,5)
		self.time_base = str(tmp[tb_str % 3] * 10 ** ((tb_str // 3) - 12)) + 's/div'
		
		self.sample_rate = str(1/horiz_interval) + 'S/sec'
		self.Ts = horiz_interval
		self.Fs = 1/horiz_interval
			
		# Reading the samples arrays
		self.fin.seek(a_comm_type)			
		self.comm_type, = unpack(bo + 'h',self.fin.read(2))
		self.fin.seek(a_wave_descriptor)
		wave_descriptor, = unpack(bo + 'l',self.fin.read(4))
		self.fin.seek(a_user_text)
		user_text, = unpack(bo + 'l',self.fin.read(4))
		self.fin.seek(a_wave_array)
		self.total_number_of_bytes, = unpack(bo + 'l',self.fin.read(4))
		self.fin.seek(a_wave_array_count)
		self.total_number_of_samples, = unpack(bo + 'l',self.fin.read(4))
		self.fin.seek(a_trigtime_array)
		trigtime_array, = unpack(bo + 'l',self.fin.read(4))
		self.fin.seek(a_subarray_count)
		self.number_of_segments, = unpack(bo + 'l',self.fin.read(4))
		
		# Calculate number of bytes per sample (should be consistent with comm_type):
		self.number_of_bytes_per_sample = int(self.total_number_of_bytes/self.total_number_of_samples)
		if (self.comm_type == 0 and self.number_of_bytes_per_sample != 1) or (self.comm_type == 1 and self.number_of_bytes_per_sample != 2):
			print('Warning (ReadTRC.read_header()): inconsistency in number of bytes per sample, file might be corrupted')
		# Calculate number of samples and bytes per segment:
		self.number_of_samples_per_segment = ceil( self.total_number_of_samples / self.number_of_segments )
		self.number_of_bytes_per_segment = self.number_of_samples_per_segment * self.number_of_bytes_per_sample
		
		# Read the contents of the trigger time_array
		if self.number_of_segments == 1: # only one segment, no trigger time array is available
			self.trigger_time = [0]
			self.trigger_offset = self.horiz_offset
			self.a_y_values = a_wave_desc + wave_descriptor + user_text
		else:
			self.fin.seek(a_wave_desc + wave_descriptor + user_text)
			trigtime_array_tmp = unpack(bo + '{}d'.format(2*self.number_of_segments),self.fin.read(16*self.number_of_segments))
			self.trigger_time = np.array(trigtime_array_tmp[0::2])
			self.trigger_offset = np.array(trigtime_array_tmp[1::2])
			self.a_y_values = a_wave_desc + wave_descriptor + user_text + trigtime_array
	    		        
		# Success
		self.fin.seek(self.a_y_values)
		self.flag_read_valid = True
		self.flag_header_read = True
		self.next_segment_counter = 0
		return 0
	
	## String representation of the settings
	# @param self The object pointer.
	def __repr__(self):
		s  = 'File name : ' + str(self.filename) + '\n'
		s += 'Instrument name : ' + str(self.instrument_name) + '\n'
		s += 'Wave source : ' + str(self.wave_source) + '\n'
		s += 'Vertical coupling : ' + str(self.vert_coupling) + '\n'
		s += 'Bandwidth limit : ' + str(self.bandwidth_limit) + '\n'
		s += 'Record type : ' + str(self.record_type) + '\n'
		s += 'Processing done : ' + str(self.processing_done) + '\n'
		s += 'Nominal bits : ' + str(self.nominal_bits) + '\n'
		s += 'Gain with_probe : ' + str(self.gain_with_probe) + '\n'
		s += 'Time base : ' + str(self.time_base) + '\n'
		s += 'Sample rate : ' + str(self.sample_rate) + '\n'
		s += 'Number of segments : ' + str(self.number_of_segments) + '\n'
		#s += 'Trigger time : ' + str(self.trigger_time) + '\n'
		#s += 'Trigger offset : ' + str(self.trigger_offset) + '\n'
		s += 'Total number of samples : ' + str(self.total_number_of_samples) + '\n'
		s += 'Number of bytes per sample : ' + str(self.number_of_bytes_per_sample) + '\n'
		s += 'Number of samples per segment : ' + str(self.number_of_samples_per_segment) + '\n\n'
		return s

	
	## Read data from the file
	# For the given indices, the data points are read from the trace file into memory
	# @param self The object pointer.
	# @param segment_number The number of the segment, where the number of the first segment is 0.
	# @param start_row The start index, i.e. the first row to be read. Default value is 0.
	# @param number_of_rows The number of rows to be read. Default value is -1 (all available rows after the given start row). If the requested number of rows exceeds the available number of rows (per segment), only the available rows are returned.
	def read_data(self,segment_number=0,start_row=0,number_of_rows=-1):
		if (segment_number >= self.number_of_segments) or (segment_number < 0):
			print('Error (ReadTRC.read_data()): requested segment does not exist')
			return -1
		# Interpret input parameters, calculate number of samples to be read:
		if number_of_rows == -1:
			number_of_samples = self.number_of_samples_per_segment-start_row # all available samples
		else:
			number_of_samples = min(number_of_rows, self.number_of_samples_per_segment-start_row)
		number_of_bytes = number_of_samples * self.number_of_bytes_per_sample # Number of data bytes to be read	
		if number_of_samples <= 0:
			print('Warning (ReadTRC.read_data(): no data has been read')
			return 0 # nothing to do
			
		# Go to the requested segment and go to the start row
		self.fin.seek(self.a_y_values + start_row*self.number_of_bytes_per_sample + segment_number*self.number_of_bytes_per_segment) 

		# The data is stored either as 8 or 16 bit integers
		if self.number_of_bytes_per_sample == 1:
			tmp_y_values = unpack(self.bo + '{}b'.format(number_of_bytes),self.fin.read(number_of_bytes))
			self.y = np.array(tmp_y_values, dtype=np.int8)
		elif self.number_of_bytes_per_sample == 2:
			#tmp_y_values = unpack(self.bo + '{}h'.format(number_of_bytes),self.fin.read(number_of_bytes))
			tmp_y_values = unpack(self.bo + '{}h'.format(number_of_samples),self.fin.read(number_of_bytes))
			self.y = np.array(tmp_y_values, dtype=np.int16)
	
		# Reconstructing and storing the samples times
		# t_rel: vector with relative time information (within segment), t_abs: absolute time with respect to first segment
		self.t_rel = (np.arange(number_of_samples) + start_row)* self.Ts + self.trigger_offset[segment_number]
		self.t_abs = self.trigger_time[segment_number]
		# Conversion from digital to analog
		self.y = self.vertical_gain * self.y - self.vertical_offset
		
		self.next_segment_counter = segment_number+1
		
		# Success
		return 0
	

	## Read data of the next segment (after the current read position) from the file
	def read_next_segment(self):
		number_of_bytes = self.number_of_samples_per_segment * self.number_of_bytes_per_sample # Number of data bytes to be read	
		
		# The data is stored either as 8 or 16 bit integers
		if self.number_of_bytes_per_sample == 1:
			tmp_y_values = unpack(self.bo + '{}b'.format(number_of_bytes),self.fin.read(number_of_bytes))
			self.y = np.array(tmp_y_values, dtype=np.int8)
		elif self.number_of_bytes_per_sample == 2:
			tmp_y_values = unpack(self.bo + '{}h'.format(self.number_of_samples_per_segment),self.fin.read(number_of_bytes))
			self.y = np.array(tmp_y_values, dtype=np.int16)
	
		# Reconstructing and storing the samples times
		# t_rel: vector with relative time information (within segment), t_abs: absolute time with respect to first segment
		self.t_rel = (np.arange(self.number_of_samples_per_segment))* self.Ts + self.trigger_offset[self.next_segment_counter]
		self.t_abs = self.trigger_time[self.next_segment_counter]
		# Conversion from digital to analog
		self.y = self.vertical_gain * self.y - self.vertical_offset
		
		self.next_segment_counter += 1
		
		# Success
		return 0


	## @var file_name
	#  The name of the file that was read
	
	## @var instrument_name
	#  The name of the instrument which recorded the data
    
	## @var wave_source
	#  The channel which was recorded

	## @var vert_coupling
	#  The vertical coupling

	## @var bandwidth_limit
	#  Wether the bandwith limit is set or not

	## @var record_type
	#  The type of recording for this set of data

	## @var processing_done
	#  The name of the processing done on the data

	## @var nominal_bits
	#  The number of bits for the vertical sampling

	## @var gain_with_probe
	#  The vertical gain, include the effect of the probe

	## @var time_base
	#  The time scale
    
	## @var sample_rate
	#  The sampling rate

	## @var number_of_segments
	# The number of recorded data segments

	## @var trigger_time
	#  The array of the trigger times for each segment of data

	## @var trigger_offset
	#  The array of the time offset for each trigger

	## @var x
	#  The numpy.ndarray holding the time (horizontal) data

	## @var y
	#  The numpy.ndarray holding the voltage (vertical) data
    
	## @var Ts
	#  Sample time (numerical value)
    
	## @var Fs
	#  Sample rate (numerical value)

	## @var flag_read_all
	#  If True, the complete file is read at once; else, data portions are read upon request.

	## @var fin_handle
	#  Handle to input file

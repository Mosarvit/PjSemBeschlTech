#!/usr/bin/python3
## @package RFTOOLS_REMOTE_LC_WAVEJET
# Python package with routines for RF remote control of AWG and DSO. 
# GSI RRF (D. Lens, 2016-2017) 

## Prerequisites:
# - NI-VISA or package PyVISA-py installed

version_string = "Rev. 0.1.17, 19.06.2018." # Based on rftools_remote, Version 0.1.16

import numpy as np
from time import sleep

try:
	import visa
except BaseException as e:
	print(e)
	print('Error (rftools_remote()): Could not load VISA package/library. Install NI-VISA or PyVISA-py.')
			
	
## Class for remote control of LeCroy WaveJet 300A Series Oscilloscopes
# Cf. also the WavJet 300A Remote Control Manual (April, 2009)
# This class has been tested with the following instruments: 
#	- LeCroy WaveJet 314A
class LeCroyWaveJet:	

	## Constructor by reading from a file
	#  @param self The object pointer.
	#  @param instrument_id Identifier string for the remote control with the instrument.
	def __init__(self, instrument_id):
	
		self.valid_connection = False
		self.instrument_id = instrument_id
		self.y = []
		self.t = []
		self.flag_valid_trigger = False
		self.flag_valid_data = False
	
	## Connect to the scope.
	#  @param self The object pointer.
	#  @param visa_option Specifies which VISA is used: 0 (default) = NI-VISA is tried first, then PyVISA-py, 1 = PyVisa-py is tried first, then NI-VISA.
	def connect(self, visa_option=0):
	
		self.visa_option = visa_option
		if self.visa_option == 1:
			try: 
				self.instrument = visa.ResourceManager('@py').open_resource(self.instrument_id)
				self.valid_connection = True   # Connection was successful
			except BaseException as e:
				print(e)
				print('\nError: Connection to the instrument using PyVisa-py failed, trying NI-VISA.\n')
				try:
					self.instrument = visa.ResourceManager().open_resource(self.instrument_id)
					self.valid_connection = True   # Connection was successful
				except BaseException as e:
					print(e)
					print('\nError: Connection to the instrument using NI-VISA failed.\n')
				
		else:
			try:
				self.instrument = visa.ResourceManager().open_resource(self.instrument_id)
				self.valid_connection = True   # Connection was successful
			except BaseException as e:
				print(e)
				print('\nError: Connection to the instrument using NI-VISA failed, trying PyVisa-py.\n')
				try:
					self.instrument = visa.ResourceManager('@py').open_resource(self.instrument_id)
					self.valid_connection = True   # Connection was successful
				except BaseException as e:
					print(e)
					print('\nError: Connection to the instrument using PyVisa-py failed.\n')
		
		if self.valid_connection:
			self.instrument.timeout = 10000
			self.write('*IDN?')
			self.idn = self.instrument.read_raw().decode("utf-8")
			self.valid_connection = True
			print('Connection to the following instrument was successful:\n ' + self.idn)
			self.write('DTFORM BYTE')							# Selects the format for sending waveform data: binary data, byte
			self.write('TRMD STOP')								# Specify trigger mode:	AUTO, NORM, SINGLE, STOP
			self.get_scope_information()
			return 0
			
		else:
			return -1
	
	
	## Disconnect from the scope.
	#  @param self The object pointer.
	def disconnect(self):
	
		self.instrument.close()
	
	
	## This functions checks whether the scope is ready for the next operation.
	def wait(self):
	
		try:
			flag_ready = 0
			while not flag_ready == 49:
				self.instrument.write('*OPC?')
				temp = self.instrument.read_raw()
				if len(temp) >= 2:
					flag_ready = temp[-2]
			return 0
		except:
			flag_ready = 0
			return 1
	
	## This function writes a command to the scope, but with a OPC? (operation complete) request beforehand to ensure that the scope is ready.
	def write(self, str):
		
		try:
			self.wait()
			self.instrument.write(str)
			return 0
		except:
			return 1
	
	## Convert a text string such as '100mV' to a float for the corresponding SI unit, i.e. 0.1 for 100 mV.
	#  @param self The object pointer.
	#  @param str A string containing the number and the unit, i.e. '100mV', '5V', '1GS', '1us'
	def convert_string_to_float(self, str):
	
		if str[-2] == 'G':
			return float(str[0:-2]) * 1e9
		elif str[-2] == 'M':
			return float(str[0:-2]) * 1e6
		elif str[-2] == 'k':
			return float(str[0:-2]) * 1e3
		elif str[-2] == 'm':
			return float(str[0:-2]) * 1e-3
		elif str[-2] == 'u':
			return float(str[0:-2]) * 1e-6
		else:
			return float(str[0:-1])
		
		
	## Read the settings from the scope
	#  @param self The object pointer.	
	def get_scope_information(self):
	
		self.write('DTINF?')
		try:
			wj_settings_list = self.instrument.read_raw().decode('utf-8')[1:-1].split(',')
		except BaseException as e:
			print(e)
			print("ERROR rftools_remote.LeCroyWaveJet.get_scope_information(): Failed to read scope settings.")
			return -1
		
		if len(wj_settings_list) == 29:
			self.number_of_channels = 4
			self.channels_string_list = ['1','2','3','4']
			index_offset = 0
		elif len(wj_settings_list) == 21:
			self.number_of_channels = 2
			self.channels_string_list = ['1','2']
			index_offset = -8
		else:
			print(len(wj_settings_list))
			print("ERROR rftools_remote.LeCroyWaveJet.get_scope_information(): Number of channels read by the DTINF? command is not supported and seems invalid.")
			return -1
		
		# get channel information (Volt per div, offset, availability)
		self.channels_V_per_div = np.ndarray(self.number_of_channels)
		self.channels_offset = np.ndarray(self.number_of_channels)
		self.channels_availability = np.zeros(self.number_of_channels)
		for chcnt in range(0,self.number_of_channels):
			self.channels_V_per_div[chcnt] = self.convert_string_to_float( wj_settings_list[4+4*chcnt][12:] )
			self.channels_offset[chcnt] = self.convert_string_to_float( wj_settings_list[5+4*chcnt][9:] )
			if wj_settings_list[6+4*chcnt][11:] == 'Available':
				self.channels_availability[chcnt] = 1
		
		self.model_name_string = wj_settings_list[0][12:]
		self.sampling_rate_string = wj_settings_list[28-index_offset][11:]
		self.sampling_rate = self.convert_string_to_float( self.sampling_rate_string )	
		self.data_record_length = int(wj_settings_list[23-index_offset][16:])
		self.time_stamp_string = wj_settings_list[27-index_offset][13:]			# format of string: hh:mm:ss.x, where x specifies tenths of a second
		self.trigger_delay = float(wj_settings_list[21-index_offset][8:-1])  	# the last character is 's' for seconds (but it is not clear whether this is always the case)
		self.time_per_division_string = wj_settings_list[20-index_offset][11:]
				
		return 0
	
	
	## Returns the actual number of samples of the current measurement
	def get_number_of_samples_per_segment(self):
		if self.get_scope_information() == 0:
			return self.data_record_length
		else:
			return -1
	
	
	## Trigger a measurement with "single" mode. 
	#  @param self The object pointer.
	#  @param channel_number This integer specifies the channel that is used for the triggering, where 1 is the first channel.
	def trigger_single(self, channel_number=1):
	
		self.flag_valid_trigger = False
		self.flag_valid_data = False
		if channel_number < 1 or channel_number > self.number_of_channels:
			print("ERROR in rftools_remote.LeCroyWaveJet.read_binary_data: Invalid channel number: "+str(channel_number)+", triggering was not possible.")
			return -1		
	
		self.write('TRMD STOP')								# stop any ongoing trigger
		self.write('TTYP EDGE')								# set trigger mode to edge
		self.write('TSLP POS')								# set trigger slope to positive
		self.write('TSRC CH' + str(channel_number))			# set trigger signal source channel to specified channel	
		print("Triggering scope ("+self.model_name_string+") on channel " + str(channel_number) + ".")
		self.write('WSGL?')
		try:
			self.instrument.read_raw()
			print("Triggering done.")
			self.flag_valid_trigger = True
			return 0
			
		except BaseException as e:
			print(e)
			print("Triggering failed.")
			return -1
	
	
	## Set horizontal range. 
	#  @param self The object pointer.
	#  @param time_per_division The time in seconds per division. The scope has 10 horizontal divisions
	def set_horizontal_range(self, time_per_division):
		
		self.write('TDIV '+str(time_per_division)+'S')
	
	
	## Set vertical range. 
	#  @param self The object pointer.
	#  @param volt_per_division Volts per division (float). The scope has 8 horizontal divisions
	#  @param channel_number An integer that specifies the channel number (it is not checked whether the value is valid). If -1 is used, all available channels are set to this vertical range.
	def set_vertical_range(self, volt_per_division, channel_number=-1):
		
		if channel_number == -1: 			# set all channels
			for channel_cnt in self.channels_string_list:
				self.write('C' + channel_cnt + ':VDIV ' + str(volt_per_division) + 'V')
		else:
			self.write('C' + str(channel_number) + ':VDIV ' + str(volt_per_division) + 'V')	
		
	
	## Change settings of an oscilloscope for calibration purposes. 
	#  @param self The object pointer.
	#  @param maximum_number_of_samples The maximum number of samples (as an integer) that the scope will record. The actual number of samples may be lower.
	def set_number_of_samples(self, maximum_number_of_samples):
		
		if maximum_number_of_samples < 1e3:					# Set maximum number of samples
			sn_string = '500'
		elif maximum_number_of_samples < 1e4:
			sn_string = '1K'
		elif maximum_number_of_samples <= 1e5:
			sn_string = '10K'
		elif maximum_number_of_samples <= 1e6:
			sn_string = '100K'
		else:
			sn_string = '500K'
		self.dtpoints_string = sn_string
		self.write('MLEN ' + self.dtpoints_string)
		self.write('DTSTART 0')								# Defines the transfer start address for waveform data transfer.
		self.write('DTPOINTS ' + self.dtpoints_string)		# Set amount of waveform data to be transferred.
		#self.write('DTPOINTS?')
		#print(self.instrument.read_raw())
	
		
	## Change basic settings of the oscilloscope. 
	#  @param self The object pointer.
	#  @param max_number_of_samples The maximum number (float) of samples that will be recorded. The value of this parameter is interpreted as follows: 0=500, 1=1K, 2=10K, 3=100K, 4=500K.
	#  @param trigger_channel Channel number of the channel to is used as trigger
	#  @param horizontal_range Horizontal range in seconds per division.
	#  @param vertical_range Vertical range in Volt per division.
	#  @param number_of_segments This parameter is ignored as the WaveJet can record only one segment.
	def setup(self, max_number_of_samples=1000, horizontal_range=1e-6, vertical_range=0.5, number_of_segments=1):
		
		temp = 'BWL '
		for channel_cnt in self.channels_string_list:
			temp += 'C' + channel_cnt + ',OFF,'
			self.write('C' + channel_cnt + ':TRA ON')		# Enables the display of all traces
			self.write('C' + channel_cnt + ':CPL D1M') 		# Set coupling to DC 1MOhm
			self.write('C' + channel_cnt + ':OFST 0MV')		# Set zero offset
		self.write(temp[0:-1])								# Disable bandwidth-limiting low-pass filter
		self.set_vertical_range(vertical_range)
		self.set_horizontal_range(horizontal_range) 		# Modifies the timebase setting
		self.set_number_of_samples(max_number_of_samples)
		self.get_scope_information()						# Refresh the scope information
		self.wait()
		
		return 0
	
		
	## Reads data from the scope and checks whether the acquisition was successful. If not, the scope is reset and the acquisition is tried again.
	def read(self, channel_number):
		
		self.read_binary_data(channel_number)
		if not self.flag_valid_data:
			print("ERROR in rftools_remote.LeCroyWaveJet.read(): Failed reading data from the scope, retrying.")
			print("Sending self-test command to scope.")
			self.write('*TST?')	
			try:
				status = self.instrument.read_raw()
			except:# BaseError as e:
				#print(e)
				print("ERROR: Failed to read from the scope.")
				return 1
			print("Status of self-test: ")
			print(status)
			#self.write('*RST')									# internal reset
			print("Closing the connection to the scope.")
			self.disconnect()
			sleep(2)
			print("Connecting to the scope again.")
			self.connect()
			sleep(2)
			
			self.read_binary_data(channel_number)
			if not self.flag_valid_data:
				print("ERROR: Failed reading data from the scope after reconnecting.")
				return -1
				
		return 0
	
	## Reads data for the scope. It is assumed that the transfer mode has been set to binary (byte), else an error will be returned.
	#  This function has been tested with the following instruments:
	#  @param self The object pointer.
	#  @param channel_number This integer specifies the channel from which data will be read. The first channel has index 1.
	def read_binary_data(self, channel_number):
		
		self.flag_valid_data = False
		
		if not self.get_scope_information() == 0:							# Refresh the scope information
			print("Error in rftools_remote.LeCroyWaveJet.read_binary_data(): Failed to refresh the scope information.")
			return -1
				
		if channel_number < 1 or channel_number > self.number_of_channels:
			print("ERROR in rftools_remote.LeCroyWaveJet.read_binary_data(): Invalid channel number: "+str(channel_number)+", no data was collected.")
			return -1
		if not self.channels_availability[channel_number-1]:
			print("ERROR in rftools_remote.LeCroyWaveJet.read_binary_data(): Channel "+str(channel_number)+" is not available (turned off or not triggered yet). No data was collected.")
			return -1
		
		self.write('WAVESRC CH' + str(int(channel_number)))
		self.write('DTWAVE?')
		rawdata = self.instrument.read_raw()
		# check first two bytes of header (should be b'\r8#', this corresponds to the byte values [13, 35, 56])
		if not rawdata[0:3] == b'\r#8' or len(rawdata) < 10: 
			print("ERROR in rftools_remote.LeCroyWaveJet.read_binary_data: Header of received data seems corrupted. Maybe transfer mode is not set to binary (byte)? No data received.")
			return -1
		# get number of data points
		total_samples = int(rawdata[3:11])
		self.t = np.ndarray(total_samples)
		self.y = np.ndarray(total_samples)
		ind1 = len(rawdata) - 11
		if ind1 >= total_samples:
			self.y[0:ind1] = np.fromstring(rawdata[11:-1], dtype='b')
		else:
			self.y[0:ind1] = np.fromstring(rawdata[11:], dtype='b')
			
			while not ind1 >= total_samples:
				rawdata = self.instrument.read_raw()
				if not rawdata:
					print("ERROR in rftools_remote.LeCroyWaveJet.read_binary_data: Received data seems corrupted.")
					return -1
				ind2 = ind1 + len(rawdata)
				if ind2 > total_samples:
					self.y[ind1:ind2] = np.fromstring(rawdata[0:-1], dtype='b')	# the very last character is a newline and will not be used.
				else:
					self.y[ind1:ind2] = np.fromstring(rawdata, dtype='b')
				ind1 = ind2
		
		# scale the sample values
		self.y = self.y / 2**7 * 4 * self.channels_V_per_div[channel_number-1] + self.channels_offset[channel_number-1]
		# make the time values array		
		self.t = np.arange(total_samples) / self.sampling_rate + self.trigger_delay
		
		self.flag_valid_data = True
		
		return 0

	
	## Returns the data (time and voltage values).
	# @param self The object pointer.
	# @param segment_number For a WaveJet scope, this parameter must be 1, because segmented measurements are not possible.
	def return_data(self, segment_number=1):
	
		if not self.flag_valid_data:
			return [], []
		else:
			if not segment_number == 1:
				print("Error in rftools_remote.LeCroyWaveRunner(): Invalid segment number: " + str(segment_number) + ". WaveJet has only one segment.")
				return [], []
			return self.t[:], self.y[:]
		
		

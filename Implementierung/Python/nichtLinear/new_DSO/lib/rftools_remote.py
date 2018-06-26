#!/usr/bin/python3
## @package RFTOOLS_REMOTE
# Python package with routines for RF remote control of AWG and DSO. 
# GSI RRF (D. Lens, 2016-2017) 

## Prerequisites:
# - NI-VISA or package PyVISA-py installed
# - Package pico-python (picoscope) installed (if using the PicoScope3000A class)

version_string = "Rev. 0.1.16, 15.11.2017." # Von Version 14, 26.09.2017

import numpy as np
#import matplotlib
#import matplotlib.pyplot as plt
from struct import unpack
from time import sleep
from math import ceil
import calendar, datetime
#import cvxopt # optimization algorithms
from time import strftime
try:
	import visa
except BaseException as e:
	print(e)
	print('Error (rftools_remote()): Could not load VISA package/library. Install NI-VISA or PyVISA-py.')


## Class for displaying available instruments
class AvailableInstruments:

	## Constructor
	#  @param self The object pointer.
	#  @param pyvisa_flag If this flag is True, PyVISA-py is used (default) to connect to the instruments. Else, NI-VISA is used.
	def __init__(self, pyvisa_flag=False):
		
		self.pyvisa_flag = pyvisa_flag
		if self.pyvisa_flag:
			self.rm = visa.ResourceManager('@py')
		else:
			self.rm = visa.ResourceManager()
		self.instrument_list = self.rm.list_resources()
		
	def print_instruments(self):
	
		print("Available Instruments:")
		print(self.instrument_list)
		
	def get_instrument_info(self):

		for instrument in self.instrument_list:
			print("")
			print("Instrument: " + instrument)
			ih = self.rm.open_resource(instrument)
			ih.write('*IDN?')
			print(ih.read_raw().decode("utf-8"))
			
	
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
		
		
## Class for remote control of LeCroy WaveRunner Oscilloscopes
# For the details of the remote control of LeCroy WaveRunner Osciloscopes, see also:
# LeCroy X-Stream Oscilloscopes, remote control manual, Feb. 2005
#  This class has been tested with the following instruments: 
#	- LeCroy WaveRunner 66Zi via USB
#	- LeCroy WaveRunner 64Xi and 44Xi via Ethernet
class LeCroyWaveRunner:	

	## Constructor by reading from a file
	#  @param self The object pointer.
	#  @param instrument_id Identifier string for the remote control with the instrument.
	def __init__(self, instrument_id, pyvisa_flag=False):
	
		self.valid_connection = False 					# This flag is set to True if a valid measurement was performed.	
		self.instrument_id = instrument_id
		self.y = []
		self.t = []
		self.flag_valid_trigger = False
		self.flag_valid_data = False

	## Connect to the scope.
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
			print('Connection to the following instrument was successful: ' + self.idn)
			self.write('CFMT DEF9,WORD,BIN')					# Selects the format for sending waveform data: binary data, word (16 bit)
			self.write('CHDR LONG')								# Set format for query responses
			self.channels_string_list = ['1','2','3','4']
			return 0
			
		else:
			return -1
	
	
	## Disconnect from the scope.
	#  @param self The object pointer.
	def disconnect(self):
	
		self.instrument.close()
	
	
	## This functions waits until the scope is ready for the next operation.
	def wait(self):
	
		flag_ready = 0
		while not flag_ready == 49:
			self.instrument.write('*OPC?')
			temp = self.instrument.read_raw()
			if len(temp) >= 2:
				flag_ready = temp[-2]
			
			
	## This function writes a command to the scope, but with a OPC? (operation complete) request beforehand to ensure that the scope is ready.
	def write(self, str):
		
		self.wait()
		self.instrument.write(str)
		
		
	## Set scope settings for real time memory mode to maximum memory
	def use_maximum_memory(self):
	
		self.write("VBS 'app.Acquisition.Horizontal.Maximize = SetMaximumMemory' ")
	
	
	## Set scope settings for real time memory mode to fixed sample rate
	def use_fixed_sample_rate(self):
	
		self.write("VBS 'app.Acquisition.Horizontal.Maximize = FixedSampleRate' ")
	
	
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
			
	
	## Change basic settings of the oscilloscope. 
	#  @param self The object pointer.
	#  @param max_number_of_samples The maximum number (float) of samples that will be recorded per segment. The value of this parameter is interpreted as follows: 0=500, 1=1K, 2=10K, 3=100K, 4=500K.
	#  @param trigger_channel Channel number of the channel to is used as trigger
	#  @param horizontal_range Horizontal range in seconds per division.
	#  @param vertical_range Vertical range in Volt per division.
	#  @param number_of_segments The number of segments (integer).
	def setup(self, max_number_of_samples=1000, horizontal_range=1e-6, vertical_range=0.5, number_of_segments=1):
	
		self.flag_calibration_done = False
		self.write('STOP') 									# Stop any ongoing measurements
		#self.write('*RST') 								# Internal reset
		temp = 'BWL '
		self.write('CFMT DEF9,WORD,BIN')					# Selects the format for sending waveform data: binary data, word (16 bit)
		self.write('CHDR LONG')								# Set format for query responses
		for channel_cnt in self.channels_string_list:
			temp += 'C' + channel_cnt + ',OFF,'
			self.write('C' + channel_cnt + ':TRA ON')		# Enables the display of all traces
			self.write('C' + channel_cnt + ':CPL D1M')		# Set coupling to DC 1MOhm
		self.write(temp[0:-1])	
		if (number_of_segments == 1):
			self.write('SEQ OFF,1')
			self.write('MSIZ ' + str(max_number_of_samples))
		else:
			self.write('SEQ ON,'+str(number_of_segments)+','+str(max_number_of_samples))	# Set sequence measurement to 'on', number of segments, max. number of samples each
		self.set_horizontal_range(horizontal_range)			# Modifies the timebase setting
		self.write('WFSU SP,0,NP,0,FP,0,SN,0')				# Specify amount of waveform data to get to controller
		self.set_vertical_range(vertical_range)
		#self.internal_calibration()
		
	## # Complete internal calibration of the oscilloscope
	#  @param self The object pointer.
	#  @param retry_number The number of retry attempts. If this is -1 (default), the calibration is retried until it is done.
	def internal_calibration(self, retry_number=-1):
		
		#self.instrument.write('ACAL OFF')			# Disable automatic calibration
		self.write('*CAL?') 
		print('DSO: calibration started')
		while self.flag_calibration_done == False:
			try:
				if self.instrument.read_raw() == b'*CAL 0\n':
					self.flag_calibration_done = True
					print('\nDSO: calibration was successful')
				else:
					print('\nDSO Error: calibration failed!')
					return -1
			except:
				print('.', end='')
				if retry_number >= 0:
					if retry_number == 0:
						break
					retry_number -= 1
							
		if not self.flag_calibration_done:
			print('Error (Remote.set_DDScalibration()): Problem occured, calibration was not possible.')
			return -1
		else:
			return 0
		
	
	## Load the template information and save to a file. This function has been tested with the following instruments: 
	#	- LeCroy WaveRunner 66Zi via USB
	#  @param self The object pointer.
	#  @param filename Filename of the textfile 
	def get_template(self, filename):
		try:
			self.write('TEMPLATE?') # Get template information
			template_info = self.instrument.read_raw() # Read the available data
		except BaseException as e:
			print(e)
			print('Error (Remote.get_template()): Problem occured.')
			return -1
		try:
			with open(filename,"wb") as fout:
				fout.write(template_info)
		except OSError as e:
			print(e)
			print('Error (Remote.get_template()): I/O problem occured.')
			return -1		
		return 0
	
	
	## Set the trigger to single and wait until the measurement ist finished and perform a measurement with single trigger mode. 
	#  @param self The object pointer.
	#  @param channel_number This integer specifies the channel that is used for the triggering, where 1 is the first channel.
	def trigger_single(self, trigger_channel=1):
		
		self.flag_valid_data = False
		self.flag_valid_trigger = False
		self.write('STOP') # Stop any ongoing measurements
		self.write('TRSE EDGE,SR,C'+str(trigger_channel)+',HT,OFF') 	# Set trigger channel
		self.write('C'+str(trigger_channel)+':TRCP DC')					# Set the coupling mode of the specified trigger source
		self.write('TRDL 0.00') 										# Set the time at which the trigger is to occur
		self.write('C'+str(trigger_channel)+':TRLV 0.0V')				# Adjust the trigger level of the specified trigger source
		self.wait()														# Wait for the setup to complete
		self.write('TRMD SINGLE') 										# Set trigger to 'single'
		#self.write('FRTR')												# Force the instrument to make one acquisition
		#self.write('WAIT 10') 											# Wait with timeout of 10 seconds
		self.write('WAIT 10')
		#self.write('*STB?')												# check if measurement was valid
		self.write('INR?')
		for cnt in range(0,5):
			try:
				rtc = int(float(self.instrument.read_raw()[5:-1].decode("utf-8")))
				#print(rtc)
				if (rtc &  1 == 1):   # new data is available
					self.flag_valid_trigger = True
					return 0
				else:
					print("DSO return code (ESR) = " + str(rtc))
					return -1
			except:
				print(".",end="")
		print("ERROR in rftools_remote.LeCroyWaveRunner.trigger_single(): Triggering failed. Timeout while waiting for the trigger of the scope.")
		return -1
	
	
	## Reads data from the scope and checks whether the acquisition was successful. If not, the scope is reset and the acquisition is tried again.
	def read(self, channel_number):
		
		self.read_binary_data(channel_number)
		if not self.flag_valid_data:
			print("ERROR in rftools_remote.LeCroyWaveRunner.read(): Failed reading data from the scope, retrying.")
			print("Sending self-test command to scope.")
			self.write('*TST?')					
			status = self.instrument.read_raw()
			print("Status of self-test: ")
			print(status)
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
		
			
	## Perform a measurement with single trigger mode and read the channel data for the specified channel from a LeCroy WaveRunner. 
	#  This function has been tested with the following instruments:
	#	- LeCroy WaveRunner 66Zi via USB
	#  Important: this function only reads out the memory for a specific channel, i.e. already recorded data. Use the "get_new_data" function  to record a new measurement on the scope.
	#  @param self The object pointer.
	#  @param channel_number 
	def read_binary_data(self, channel_number):
		try:
			self.write('C' + str(channel_number) +':WAVEFORM?')
			rawdata = self.instrument.read_raw()
		except BaseException as e:
			print(e)
			#print('Error (Remote.read_raw_data()): Remote control problem occured.')
			self.flag_valid_data = False		# data is not valid
			return -1
				
		# now interpret the raw data occording to the LECROY_2_3 template:	
		# Look for the beginning of the header
		a_wave_desc = rawdata[0:50].find(b'WAVEDESC',0,50)
		
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
		comm_order = unpack('h',rawdata[a_comm_order:a_comm_order+2])
		# Byte ordering string for the unpacking options
		if comm_order:
				bo = '<'
		else:
			bo = '>'
		self.comm_order = comm_order

		# Read and store the options, instrument name and date
		self.instrument_name, = unpack(bo + '16s',rawdata[a_instrument_name:a_instrument_name+16])
		self.instrument_number, = unpack(bo + 'l',rawdata[a_instrument_number:a_instrument_number+4])
		secs,mins,hours,days,months,years, = unpack(bo + 'd4bh',rawdata[a_trigger_time:a_trigger_time+14])		
		self.time_of_measurement = '{}.{}.{}, {}:{}:{}'.format(days, months,years, hours, mins, secs)

		tmp = ('channel 1', 'channel 2', 'channel 3', 'channel 4', 'unknown')
		self.wave_source = tmp[unpack(bo + 'h',rawdata[a_wave_source:a_wave_source+2])[0]]
		tmp = ('DC_50_Ohms', 'ground','DC 1MOhm','ground','AC 1MOhm')
		self.vert_coupling = tmp[unpack(bo + 'h',rawdata[a_vert_coupling:a_vert_coupling+2])[0]]
		tmp = ('off', 'on ')
		self.bandwidth_limit = tmp[unpack(bo + 'h',rawdata[a_bandwidth_limit:a_bandwidth_limit+2])[0]]
		tmp = ( 'single_sweep',    'interleaved', 'histogram', 'graph', 'filter_coefficient', 'complex', 'extrema',  'sequence_obsolete', 'centered_RIS', 'peak_detect')
		self.record_type = tmp[unpack(bo + 'h',rawdata[a_record_type:a_record_type+2])[0]]
		tmp = ('no_processing', 'fir_filter', 'interpolated', 'sparsed', 'autoscaled', 'no_result', 'rolling', 'cumulative')
		self.processing_done = tmp[unpack(bo + 'h',rawdata[a_processing_done:a_processing_done+2])[0]]

		# Reading and storing the vertical settings
		tmp = (1,2,5)
		fvg_str, = unpack(bo + 'h',rawdata[a_fixed_vert_gain:a_fixed_vert_gain+2])
		fixed_vertical_gain=tmp[fvg_str % 3] * 10 ** ((fvg_str // 3) - 6)
		probe_att, = unpack(bo + 'f',rawdata[a_probe_att:a_probe_att+4])
		self.vertical_gain, = unpack(bo + 'f',rawdata[a_vertical_gain:a_vertical_gain+4])
		self.vertical_offset, = unpack(bo + 'f',rawdata[a_vertical_offset:a_vertical_offset+4])
		self.nominal_bits, = unpack(bo + 'h',rawdata[a_nominal_bits:a_nominal_bits+2])
		self.gain_with_probe = str(fixed_vertical_gain*probe_att) + 'V/div'
		
		# Reading and storing the horizontal settings
		horiz_interval, = unpack(bo + 'f',rawdata[a_horiz_interval:a_horiz_interval+4])
		horiz_offset, = unpack(bo + 'd',rawdata[a_horiz_offset:a_horiz_offset+8]) # trigger offset for the first sweep of the trigger
		tb_str, = unpack(bo + 'h',rawdata[a_fixed_vert_gain:a_fixed_vert_gain+2])
		tmp = (1,2,5)
		self.time_base = str(tmp[tb_str % 3] * 10 ** ((tb_str // 3) - 12)) + 's/div'
		self.sample_rate = str(1/horiz_interval) + ' S/sec'
		self.Ts = horiz_interval
		self.Fs = 1/horiz_interval
		
		# Reading the samples arrays
		self.comm_type, = unpack(bo + 'h',rawdata[a_comm_type:a_comm_type+2])
		wave_descriptor, = unpack(bo + 'l',rawdata[a_wave_descriptor:a_wave_descriptor+4])
		user_text, = unpack(bo + 'l',rawdata[a_user_text:a_user_text+4])
		self.total_number_of_bytes, = unpack(bo + 'l',rawdata[a_wave_array:a_wave_array+4])
		self.total_number_of_samples, = unpack(bo + 'l',rawdata[a_wave_array_count:a_wave_array_count+4])
		trigtime_array, = unpack(bo + 'l',rawdata[a_trigtime_array:a_trigtime_array+4])
		self.number_of_segments, = unpack(bo + 'l',rawdata[a_subarray_count:a_subarray_count+4])
		
		# Calculate number of bytes per sample (should be consistent with comm_type):
		if self.total_number_of_samples == 0:
			self.flag_valid_data = False
			if self.comm_type == 0:
				self.number_of_bytes_per_sample = 1
			elif self.comm_type == 1:
				self.number_of_bytes_per_sample = 2
			self.number_of_samples_per_segment = 0
			self.number_of_bytes_per_segment = 0
			self.y = []
			self.t = []
			self.trigger_time = []
			self.trigger_offset = []
			return 0
			
		self.number_of_bytes_per_sample = int(self.total_number_of_bytes/self.total_number_of_samples)
		if (self.comm_type == 0 and self.number_of_bytes_per_sample != 1) or (self.comm_type == 1 and self.number_of_bytes_per_sample != 2):
			print('Warning (Remote.read_data_WR()): inconsistency in number of bytes per sample, file might be corrupted')
		# Calculate number of samples and bytes per segment:
		self.number_of_samples_per_segment = ceil( self.total_number_of_samples / self.number_of_segments )
		self.number_of_bytes_per_segment = self.number_of_samples_per_segment * self.number_of_bytes_per_sample

		# Prepare the data vectors
		self.t = np.zeros((self.number_of_segments,self.number_of_samples_per_segment))
		self.y = np.zeros((self.number_of_segments,self.number_of_samples_per_segment))
		
		# Read the trigger time array and the data
		a_y_values = a_wave_desc + wave_descriptor + user_text + trigtime_array
		if self.number_of_segments == 1: 
		# only one segment, no trigger time array is available, read data
			self.trigger_time = [0]
			self.trigger_offset = [horiz_offset]
			if self.comm_type == 0: # byte
				tmp_y_values = unpack(bo + '{}b'.format(self.total_number_of_samples),rawdata[a_y_values:a_y_values+self.total_number_of_bytes])
				self.y[0,:] = np.array(tmp_y_values, dtype=np.int8)
			else: # word
				tmp_y_values = unpack(bo + '{}h'.format(self.total_number_of_samples),rawdata[a_y_values:a_y_values+self.total_number_of_bytes])
				self.y[0,:] = np.array(tmp_y_values, dtype=np.int16)
			# Reconstructing and storing the samples times
			self.t[0,:] = np.arange(self.total_number_of_samples) * self.Ts + self.trigger_offset
		else:
		# more than one segment, read trigger time array and then data
			a_triggers = a_wave_desc + wave_descriptor + user_text
			trigtime_array_tmp = unpack(bo + '{}d'.format(2*self.number_of_segments),rawdata[a_triggers:a_triggers+16*self.number_of_segments])
			self.trigger_time = np.array(trigtime_array_tmp[0::2]) # trigger time of the segment with respect to the first segment
			self.trigger_offset = np.array(trigtime_array_tmp[1::2]) # trigger offset of the segments
			if self.comm_type == 0: # byte
				tmp_y_values = unpack(bo + '{}b'.format(self.total_number_of_samples),rawdata[a_y_values:a_y_values+self.total_number_of_bytes])
				self.y[:,:] = np.array(tmp_y_values, dtype=np.int8).reshape(self.number_of_segments, self.number_of_samples_per_segment)
			else: # word
				tmp_y_values = unpack(bo + '{}h'.format(self.total_number_of_samples),rawdata[a_y_values:a_y_values+self.total_number_of_bytes])
				self.y[:,:] = np.array(tmp_y_values, dtype=np.int16).reshape(self.number_of_segments, self.number_of_samples_per_segment)
            # Reconstructing and storing the sample times			
			# Important! The following time vector does not contain the trigger_time, i.e. the time with respect to the first segment.
			# Therefore, it is only a relative time within each segment!
			self.t[:,:] = np.tile((self.trigger_offset).reshape(-1,1),(1,self.number_of_samples_per_segment)) + np.tile((np.arange(self.number_of_samples_per_segment) * self.Ts),(self.number_of_segments,1))
			
			
		# Conversion from digital to analog
		self.y = self.vertical_gain * self.y - self.vertical_offset
		
		self.flag_valid_data = True
		
		return 0	
	
	
	## Returns the actual number of samples of the current measurement
	def get_number_of_samples_per_segment(self):
		if self.flag_valid_data:
			return self.number_of_samples_per_segment
		else:
			return -1
	
	
	## Returns the data (time and voltage values) of a specific segment.
	# @param self The object pointer.
	# @param segment_number Specifies the segment, where the first segment has index 1.
	def return_data(self, segment_number=1):
	
		if not self.flag_valid_data:
			return [], []
		else:
			if segment_number < 1 or segment_number > self.number_of_segments:
				print("Error in rftools_remote.LeCroyWaveRunner(): Invalid segment number: " + str(segment_number) + ". Valid numbers are from 1 to " + str(self.number_of_segments) + ".")
				return [], []
			return self.t[segment_number-1,:]+self.trigger_time[segment_number-1], self.y[segment_number-1,:]
	
	
	## Defines the string that is printed when using the 'print()' command on an instance of this class.
	# @param self The object pointer.
	def __repr__(self):
		if not hasattr(self,'instrument_name'):
			if self.read_data(1) == -1:
				return 'Error (RemoteWaveRunner): No connection to the device.'
		s = 'Instrument ID: ' + str(self.instrument_id) + '\n'
		s += 'Instrument name: ' + str(self.instrument_name) + '\n'
		s += 'Instrument number: ' + str(self.instrument_number) + '\n'
		s += 'Time of last measurement: ' + str(self.time_of_measurement) + '\n'
		s += 'Wave source: ' + str(self.wave_source) + '\n'
		s += 'Vertical coupling: ' + str(self.vert_coupling) + '\n'
		s += 'Bandwidth limit: ' + str(self.bandwidth_limit) + '\n'
		s += 'Record type: ' + str(self.record_type) + '\n'
		s += 'Processing: ' + str(self.processing_done) + '\n'
		s += 'Vertical gain: ' + str(self.vertical_gain) + '\n'
		s += 'Vertical offset: ' + str(self.vertical_offset) + '\n'
		s += 'Nominal bits: ' + str(self.nominal_bits) + '\n'
		s += 'Gain with probe: ' + str(self.gain_with_probe) + '\n'
		s += 'Time base: ' + str(self.time_base) + '\n'
		s += 'Sample rate: ' + str(self.sample_rate) + '\n'
		s += 'Sample time in seconds: ' + str(self.Ts) + '\n'
		s += 'Subformat (0: byte, 1: word): ' + str(self.comm_type) + '\n'
		s += 'Total number of bytes: ' + str(self.total_number_of_bytes) + '\n'
		s += 'Total number of samples: ' + str(self.total_number_of_samples) + '\n'
		s += 'Number of segments: ' + str(self.number_of_segments) + '\n'
		s += 'Number of samples per segment : ' + str(self.number_of_samples_per_segment) + '\n'
		s += 'Trigger time: ' + str(self.trigger_time) + '\n'
		s += 'Trigger offset: ' + str(self.trigger_offset) + '\n'
		return s
		
	
	## @var instrument
	#  Ressource data structure for the connection to the instrument.
	## @var instrument_id
	#  String with remote control ID of the instrument.

	
## Class for remote control of waveform generator (Agilent)
# For the details of the remote control of Agilent AWGs, see also:
# Agilent 33220A User's Guide, Agilent Technologies, 2007.
# Agilent 33500 Series 30 MHz Funtion / AWG, User's Guide, Agilent Technologies, 2010.
#  This class has been tested with the following instruments: 
#	- Agilent 33521A AWG
class Agilent:	

	## Constructor
	#  @param self The object pointer.
	#  @param instrument_id Identifier string for the remote control with the instrument.
	def __init__(self, instrument_id, pyvisa_flag=False):
		self.valid_connection = False # This flag is set to True if a valid measurement was performed.	
		self.instrument_id = instrument_id
		self.pyvisa_flag = pyvisa_flag
	
	
	## Connect to the scope.
	#  @param self The object pointer.
	def connect(self):
	
		if self.pyvisa_flag:
			try: 
				self.instrument = visa.ResourceManager('@py').open_resource(self.instrument_id)
				self.valid_connection = True   # Connection was successful
			except BaseException as e:
				print(e)
				print('Error: Connection to the instrument using Pyvisa-py failed. Available instruments are:')
				print(visa.ResourceManager().list_resources())
				
		else:
			try:
				self.instrument = visa.ResourceManager().open_resource(self.instrument_id)
				self.valid_connection = True   # Connection was successful
			except BaseException as e:
				print(e)
				print('Error: Connection to the instrument using NI-VISA failed. Available instruments are:')
				print(visa.ResourceManager().list_resources())
		
		if self.valid_connection:
			self.instrument.timeout = 10000
			self.instrument.write('*IDN?')
			self.idn = self.instrument.read_raw().decode("utf-8")
			self.valid_connection = True
			print('Connection to the following instrument was successful: ' + self.idn)
			#print('Connection to the instrument ' + self.instrument.manufacturer_name + ' ' + self.instrument.model_name +  ' was successful.')		
			return 0
			
		else:
			return -1

	
	## This functions waits until the instrument is ready for the next operation.
	def wait(self):
	
		flag_ready = 0
		while not flag_ready == 49:
			self.instrument.write('*OPC?')
			temp = self.instrument.read_raw()
			if len(temp) >= 2:
				flag_ready = temp[-2]
				
	
	## Turns a channel	on or off.
	#  @param self The object pointer.
	#  @param flag_set_on If True, the channel is set to ON, else it is set to OFF.
	#  @param channel_number The number of the output channel (1 is default). Note: It is not checked whether the channel exists for the connected waveform generator.
	def output_on_off(self, flag_set_on, channel_number=1):
	
		if flag_set_on:
			self.instrument.write('OUTPut'+str(channel_number)+' ON')
		else:
			self.instrument.write('OUTPut'+str(channel_number)+' OFF')
		self.wait()
	
	
	## Sets output channel 1 or 2 to dual mode, tracking, identical or inverted
	#  @param mode Tracking mode, can be 'on', 'off', or 'inverted'.
	def set_tracking(self, mode):
		
		if mode == 'off':
			self.instrument.write('SOURce2:TRACk OFF')
		elif mode == 'inverted':
			self.instrument.write('SOURce2:TRACk INV')
		elif mode == 'on':
			self.instrument.write('SOURce2:TRACk ON')
		else:
			print("rftools_remote.Agilent.set_tracking(): Unknown tracking mode.")
		self.wait()
	
	
	## Sets the output impedance of a channel.
	#  @param self The object pointer.
	#  @param load_impedance A string defining the desired load impedance configuration. Possible values are: '50' (50 Ohms) and 'INF' (high impedance).
	#  @param channel_number The number of the output channel (1 is default). Note: It is not checked whether the channel exists for the connected waveform generator.
	def set_load_impedance(self, load_impedance, channel_number=1):
	
		if load_impedance == '50':
			self.instrument.write('OUTPut'+str(channel_number)+':LOAD 50')
		elif load_impedance == 'INF':
			self.instrument.write('OUTPut'+str(channel_number)+':LOAD INF')
		else:
			print('Error (Remote.Agilent.set_load_impedance()): Unknown load impedance ' + load_impedance)
			return -1
		return 0
	
	
	## Set a channel to DC voltage mode. For a high load impedance (cf. parameter load_impedance), the permissible voltage range is -10V to 10V. For a 50 Ohm load impedance, it is -5V to 5V.
	#  @param self The object pointer.
	#  @param dc_voltage The desired voltage in Volt as a floating point number.
	#  @param channel_number The number of the output channel (1 is default) as an integer. Note: It is not checked whether the channel exists for the connected waveform generator.
	#  @param load_impedance A string defining the desired load impedance configuration. Possible values are: '50' and 'INF'
	def DC_voltage(self, dc_voltage, channel_number=1, load_impedance='INF'):
	
		if not self.set_load_impedance(load_impedance, channel_number) == 0:
			return -1
		if load_impedance == '50' and abs(dc_voltage) > 5:
			print('Error (Remote.Agilent.DC_voltage()): DC voltage has to be within -5V to 5V for a load impedance of 50 Ohms.')
			return -1
		if load_impedance == 'INF' and abs(dc_voltage) > 10:
			print('Error (Remote.Agilent.DC_voltage()): DC voltage has to be within -10V to 10V for a high load impedance.')
			return -1
		try:
			self.instrument.write('SOUR'+str(channel_number)+':FUNC DC')
			self.instrument.write('VOLTage:OFFSet '+str(dc_voltage))
			self.wait()
		except BaseException as e:
			print(e)
			print('Error (Remote.Agilent.DC_voltage()): Problem occured.')
			return -1
		return 0
		
		
	## Set a channel to sine output mode. The offset voltage is set to zero.
	#  @param self The object pointer.
	#  @param amplitude_peak The desired peak amplitude Volt as a floating point number. Note: It is not checked whether the amplitude value is within the admissable range.
	#  @param frequency The desired frequency in Hz.
	#  @param channel_number The number of the output channel (1 is default) as an integer. Note: It is not checked whether the channel exists for the connected waveform generator.
	#  @param load_impedance A string defining the desired load impedance configuration. Possible values are: '50' and 'INF'
	def sine(self, amplitude_peak, frequency, channel_number=1, load_impedance='50'):
		if not self.set_load_impedance(load_impedance, channel_number) == 0:
			return -1
		if load_impedance == '50' and abs(amplitude_peak) > 5:
			print('Error (Remote.Agilent.sine()): The amplitude is limited to 5Vp for a load impedance of 50 Ohms.')
			return -1
		if load_impedance == 'INF' and abs(amplitude_peak) > 10:
			print('Error (Remote.Agilent.sine()): The amplitude is limited to 10Vp for a high load impedance.')
			return -1
		try:
			self.instrument.write('SOUR'+str(channel_number)+':FREQ ' + str(frequency))
			self.instrument.write('SOUR'+str(channel_number)+':VOLTage ' + str(amplitude_peak*2))
			self.instrument.write('SOUR'+str(channel_number)+':VOLTage:OFFSet ' + str(0))
			self.instrument.write('SOUR'+str(channel_number)+':FUNC SIN')
			self.wait()
		except BaseException as e:
			print(e)
			print('Error (Remote.Agilent.sine()): Problem occured.')
			return -1
		return 0
	
	## @var instrument
	#  Ressource data structure for the connection to the instrument.
	## @var instrument_id
	#  String with remote control ID of the instrument.	
	

class PicoScope3000A:
	
	## Constructor for remote control of PicoScope 3000A series.
	#  @param self The object pointer.
	#  @param instrument_id	The serial number of the scope as a string, e.g. 'C0127/184'. If no string is specified, it is tried to detect the scope automatically.
	def __init__(self, instrument_id=''):
		
		self.valid_connection = False
		self.instrument_id = instrument_id
				
	## Connect to a scope
	#  @param self The object pointer.
	#  @param instrument_id	The serial number of the scope as a string, e.g. 'C0127/184'. If no string is specified, it is tried to detect the scope automatically.
	def connect(self):
	
		try:
			if self.instrument_id:
				self.ps = picoscope.ps3000a.PS3000a(connect=False)
				self.ps.open( bytearray(self.instrument_id+'\x00','utf8') )
			else:
				self.ps = picoscope.ps3000a.PS3000a(connect=True)
		except BaseException as e:
			print(e)
			print("ERROR (class rftools_remote.PicoScope3000A): Unable to connect to the scope.")
			return -1
		
		else:
			print("ERROR (class rftools_remote.PicoScope3000A): Unknown or not supported type: " + self.instrument_type)
			return -1
	
		self.valid_connection = True
		return 0
	
	## Set the channel settings
	#  @param self The object pointer.
	def set_channels_default(self):
		
		for channel_cnt in ['A','B','C','D']:
			self.ps.setChannel(channel=channel_cnt, coupling='DC', VRange=1)
		
		ps.setSimpleTrigger(channel='A', threshold_V=0.0, timeout_ms=1000)
		
		return 0
	
	## Make a single measurement
	#  @param self The object pointer.
	def measure(self):
		
		sampling_frequency = 200e6
		sampling_interval = 10e-6
		
		time_info = self.ps.setSamplingInterval( 1/sampling_frequency, sampling_interval )
		self.ps.runBlock(pretrig=0.5) 		# pre-trigger in percentage of the sampled interval
		self.t = time_info[0]				# array with time values
		self.y = self.ps.getDataV('A')[0]	# array with vertical values of first channel
		for channel_cnt in ['B','C','D']:
			self.y = np.column_stack( (self.y, self.ps.getDataV(channel_cnt)[0]) )
		
		return 0
	## 
	#  

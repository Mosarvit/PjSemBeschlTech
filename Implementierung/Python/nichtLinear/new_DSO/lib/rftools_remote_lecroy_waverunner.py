#!/usr/bin/python3
## @package RFTOOLS_REMOTE_LC_WAVERUNNER
# Python package with routines for RF remote control of LeCroy WaveRunner oscilloscopes.
# GSI RRF (D. Lens, A. Andreev, 2018) 

## Prerequisites:
# - NI-VISA or package PyVISA-py installed

version_string = "Rev. 0.0.3, 19.06.2018."

# History:
# Rev. 0.0.3: - Partially tested with HDO8058A (8 channels)

import numpy as np
from struct import unpack
from time import sleep
from math import ceil
try:
	import visa
except BaseException as e:
	print(e)
	print('Error (rftools_remote()): Could not load VISA package/library. Install NI-VISA or PyVISA-py.')

		
## Class for remote control of LeCroy WaveRunner Oscilloscopes
# For the details of the remote control of LeCroy WaveRunner Osciloscopes, see also:
# LeCroy X-Stream Oscilloscopes, remote control manual, Feb. 2005
#  This class has been tested with the following instruments: 
#	- LeCroy WaveRunner 66Zi via USB
#	- LeCroy WaveRunner 64Xi and 44Xi via Ethernet
#   - LeCroy HDO8058A via USB
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
	# Channels_string_list is a list with available channel numbers (e.g. ['1','2','3','4'])
	def connect(self, visa_option=0, channels_string_list = ['1','2','3','4']):
	
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
			self.channels_string_list = channels_string_list
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
	
	
	# Sets real time memory mode to maximum memory or fixed sample rate
	def use_maximum_memory(maximum_memory = True):
		if maximum_memory: 
			self.write("VBS 'app.Acquisition.Horizontal.Maximize = SetMaximumMemory' ")
		else:
			self.write("VBS 'app.Acquisition.Horizontal.Maximize = FixedSampleRate' ")
	
	# Sets maximum number of samples
	def set_maximum_number_of_samples(max_number_of_samples=1000):
		self.write('MSIZ ' + str(max_number_of_samples))
	
	
	# Sets DSO to Realtime Sampling Mode (one segment)
	def set_realtime_mode():
		self.write('SEQ OFF,1')
		
	
	# Sets DSO to sequential mode (several segments)
	def set_sequential_mode(number_of_segments, max_number_of_samples_per_segment):
		self.write('SEQ ON,'+str(number_of_segments)+','+str(max_number_of_samples_per_segment))	# 
		
	
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
		self.use_maximum_memory()
		for channel_cnt in self.channels_string_list:
			temp += 'C' + channel_cnt + ',OFF,'
			self.write('C' + channel_cnt + ':TRA ON')		# Enables the display of all traces
			self.write('C' + channel_cnt + ':CPL D1M')		# Set coupling to DC 1MOhm
			self.write('C' + channel_cnt + ':OFST 0')		# Set zero offset
		self.write(temp[0:-1])	
		if (number_of_segments == 1):
			self.write('SEQ OFF,1')
			self.write('MSIZ ' + str(max_number_of_samples))
		else:
			self.write('SEQ ON,'+str(number_of_segments)+','+str(max_number_of_samples))	# Set sequence measurement to 'on', number of segments, max. number of samples each
		self.set_horizontal_range(horizontal_range)			# Modifies the timebase setting
		self.write('WFSU SP,0,NP,0,FP,0,SN,0')				# Specify amount of waveform data to get to controller
		self.set_vertical_range(vertical_range)
		self.write('GRID QUAD')
		self.internal_calibration()
		
		
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
	def trigger_single(self, trigger_channel=1, trigger_level = 0.0):
		
		self.flag_valid_data = False
		self.flag_valid_trigger = False
		self.write('STOP') # Stop any ongoing measurements
		self.write('TRSE EDGE,SR,C'+str(trigger_channel)+',HT,OFF') 	# Set trigger channel
		self.write('C'+str(trigger_channel)+':TRCP DC')					# Set the coupling mode of the specified trigger source
		self.write('TRDL 0.00') 										# Set the time at which the trigger is to occur
		self.write('C'+str(trigger_channel)+':TRLV '+str(trig_lvl))		# Adjust the trigger level of the specified trigger source
		self.wait()														# Wait for the setup to complete
		self.write('TRMD SINGLE') 										# Set trigger to 'single'
		#self.write('FRTR')												# Force the instrument to make one acquisition
		self.write('WAIT 10') 											# Wait with timeout of 10 seconds
		self.instrument.write('Time_DIV?') #get the timebase
		temp = self.instrument.read_raw()
		temp = temp.decode("utf-8")
		temp2 = temp.split(" ")
		self.time_base_used = float(temp2[1])
		#self.write('*STB?')											# check if measurement was valid
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
		
	
	## Sets sequential trigger
	## Be careful: Function TRSE has reversed order for Qualified Trigger. First condition should be QL, Second condition -- SR
	## pretrig -- always 5% of the whole interval
	def trigger_sequential(self,trigger_channel1=1, trig_lvl1=0.0, trigger_channel2=2, trig_lvl2=0.0,n_events=0,pretrig=0):

		self.flag_valid_data = False
		self.flag_valid_trigger = False
		self.write('STOP')  # Stop any ongoing measurements
		#self.write('TRSE TEQ,SR,C'+str(trigger_channel2)+',QL,C'+str(trigger_channel1)+',HT,OFF') # Sets Edge Qualified Trigger
		if n_events!=0:
			self.write('TRSE TEQ,SR,C' + str(trigger_channel2) + ',QL,C' + str(
						trigger_channel1) + ',HT,EV,HV,'+str(n_events))  # Sets Edge Qualified Trigger
		else:
			self.write('TRSE TEQ,SR,C'+str(trigger_channel2)+',QL,C'+str(trigger_channel1)+',HT,OFF') # Sets Edge Qualified Trigger

		##self.write('TRSE?')
		##rtc = self.instrument.read_raw().decode("utf-8")
		##self.wait()
		for chan in [trigger_channel1,trigger_channel2]:
			self.write('C' + str(chan) + ':TRCP DC')  									  # Set the coupling mode of the specified trigger source
			self.write('C' + str(chan) + ':TRSL POS')									  # Set trigger positive slope
		self.write('C' + str(trigger_channel1) + ':TRLV ' + str(
					trig_lvl1))  														  # Adjust the trigger level of the specified trigger source
		self.write('C' + str(trigger_channel2) + ':TRLV ' + str(
					trig_lvl2))  														  # Adjust the trigger level of the specified trigger source

		#self.write('''VBS 'app.Acquisition.Trigger.HoldoffType = "Events"' ''')
		#self.instrument.write('TRIG_SELECT?')
		#temp=self.instrument.read_raw().decode("utf-8")


		self.instrument.write('Time_DIV?') #get the timebase
		self.time_base_used = float(self.instrument.read_raw().decode('utf-8').split(" ")[1])
		if pretrig != 0:																  # Set the time at which the trigger is to occur
			#self.instrument.write('TRDL ' + str(-(self.time_base_used * 5 - self.time_base_used * 5 / 100 * 5)))
			self.instrument.write('TRDL ' + str(-(self.time_base_used * 5*(1-pretrig)))) # WORKS
			#self.instrument.write('TRDL ' + str(-(self.time_base_used*100/50)))
		else:
			self.write('TRDL 0.00')
		self.wait()  																	  # Wait for the setup to complete
		self.write('TRMD SINGLE')  														  # Set trigger to 'single'
		#self.write('WAIT 10')
		# self.write('*STB?')															  # check if measurement was valid
		self.write('INR?')
		for cnt in range(0, 5):
			try:
				rtc = int(float(self.instrument.read_raw()[5:-1].decode("utf-8")))
				# print(rtc)
				if (rtc & 1 == 1):  # new data is available
					self.flag_valid_trigger = True
					return 0
				else:
					print("DSO return code (ESR) = " + str(rtc))
					return -1
			except:
				print(".", end="")
		print(
			"ERROR in rftools_remote.LeCroyWaveRunner.trigger_single(): Triggering failed. Timeout while waiting for the trigger of the scope.")
		return -1
	
	## Arms the scope and does the new measurement 	
	def get_new_data(self):
	
		self.flag_valid_data = False
		self.write('STOP') # Stop any ongoing measurements
		self.write('ARM')  # Arms the scope -- changes acquisition from STOP to SINGLE
		self.write('WAIT 10')
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
		print("ERROR in rftools_remote.LeCroyWaveRunner.get_new_data(): Get new data failed")
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

		tmp = ('channel 1', 'channel 2', 'channel 3', 'channel 4', 'channel 5', 'channel 6', 'channel 7', 'channel 8', 'unknown')
		self.wave_source = tmp[unpack(bo + 'h',rawdata[a_wave_source:a_wave_source+2])[0]]
		tmp = ('DC_50_Ohms', 'ground','DC 1MOhm','ground','AC 1MOhm')
		self.vert_coupling = tmp[unpack(bo + 'h',rawdata[a_vert_coupling:a_vert_coupling+2])[0]]
		tmp = ('off', 'on ')
		self.bandwidth_limit = tmp[unpack(bo + 'h',rawdata[a_bandwidth_limit:a_bandwidth_limit+2])[0]]
		tmp = ('single_sweep', 'interleaved', 'histogram', 'graph', 'filter_coefficient', 'complex', 'extrema',  'sequence_obsolete', 'centered_RIS', 'peak_detect')
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

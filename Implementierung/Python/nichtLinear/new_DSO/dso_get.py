#!/usr/bin/python3
# STARFISH-PY: Software Tools for Accelerator RF Instrumentation via Command Shell using Python

revision_string = '0.3.2, 19.06.2018'

#    STARFISH-PY, DSO_GET: <Short description>.
#    Copyright (C) 2018  GSI, D. Lens

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

import numpy as np
import lib.rftools_misc as rftools_misc
import lib.rftools_bcf as rftools_bcf
import lib.rftools_remote as rftools_remote
import lib.rftools_csv as rftools_csv
import sys, glob, argparse, colorama, configparser
import matplotlib.pyplot as plt
import time

# Initialization of colored text output:
colorama.init()

# Parse the command line arguments:
parser = argparse.ArgumentParser(description='RF tools, DSO_GET. Reads the sample data of one or more channel(s) of a digital storage oscilloscope of the LeCroy WaveRunner or WaveJet type. Revision: ' + revision_string + '.')
parser.add_argument('-r', action="store", dest="dso_id", default='', help="Instrument remote ID string of the scope. If an INI-file is used, the ID in the INI file overwrites the ID from this key.")
parser.add_argument('-t', action="store", dest="dso_type", default='1', help="Type of DSO: 1 (LeCroy Wavejet), 2 (LeCroy Waverunner). Default: 1.")
parser.add_argument('-o', action="store", dest="output_file_name", default='dso.bcf', help="Output file name. Default: dso.bcf.")
parser.add_argument('-d', action="store", dest="data_type", default='0', help='Specifies the data type that is used to save the data: 0 (float), 1 (double). Default is 0.')
parser.add_argument('-c', action="store", dest="channels", default='1-4', help="Specifies the channels of the scope that will be read out. Examples: '-c 1,2,4', '-c 2-4'. Default is 1-4.")
parser.add_argument('-s', action="store", dest="number_of_segments", default='1', help="Specifies the number of segments. Default: 1.")
parser.add_argument('-n', action="store", dest="number_of_samples", default='1e3', help="Number of samples per segment. Default: 1e3.")
parser.add_argument('-vr', action="store", dest="vertical_range", default='1', help="Vertical range: Volt per division. Default: 1.")
parser.add_argument('-hr', action="store", dest="horizontal_range", default='1', help="Horizontal range: Seconds per division. Default: 1e-6.")
parser.add_argument('-tr', action="store_true", dest="trigger", default=False, help="Triggers before reading the scope data. Default: No triggering (direct readout of channel data).")
parser.add_argument('-tc', action="store", dest="trigger_channel", default='1', help="Specifies the trigger channel. Default: 1.")
parser.add_argument('-i', action="store", dest="ini_file", default='', help="INI-file with settings. This option overwrites the other options.")
parse_result = parser.parse_args(sys.argv[1:])

print(colorama.Back.GREEN + colorama.Style.BRIGHT + "DSO_GET: Start." + colorama.Style.NORMAL + colorama.Back.RESET)

# Default values:
dso_id = ''
dso_type = 'wavejet'
channels = [1,2,3,4]
number_of_segments = 1
maximum_number_of_samples_per_segment = 1e3
scope_vertical_range_volt_per_div = 1
scope_horizontal_range_time_per_div = 1e-6
trigger = 'no'
trigger_channel = 1
output_file_name = 'dso.bcf'
file_type = 'bcf'

if parse_result.ini_file == '':
	dso_id = parse_result.dso_id
	try:
		channels = rftools_misc.expand_mixrange(parse_result.channels)
	except:
		print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: Invalid input parameter for the channels." + colorama.Style.NORMAL + colorama.Back.RESET)
		sys.exit(10)
	try:
		number_of_segments = int(parse_result.number_of_segments)
	except:
		print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: Invalid input parameter for the number of segments." + colorama.Style.NORMAL + colorama.Back.RESET)
		sys.exit(10)		
	try:
		maximum_number_of_samples_per_segment = int(float(parse_result.number_of_samples))
	except:
		print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: Invalid input parameter for the number of samples." + colorama.Style.NORMAL + colorama.Back.RESET)
		sys.exit(10)
	try:
		scope_vertical_range_volt_per_div = float(parse_result.vertical_range)
	except:
		print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: Invalid input parameter for the vertical range (no float?)." + colorama.Style.NORMAL + colorama.Back.RESET)
		sys.exit(10)	
	try:
		scope_horizontal_range_time_per_div = float(parse_result.horizontal_range)
	except:
		print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: Invalid input parameter for the horizontal range (no float?)." + colorama.Style.NORMAL + colorama.Back.RESET)
		sys.exit(10)	
	if parse_result.trigger:
		trigger = 'yes'
	else:
		trigger = 'no'
	try:
		trigger_channel = int(parse_result.trigger_channel)
	except:
		print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: Invalid input parameter for the trigger channel (no integer?)." + colorama.Style.NORMAL + colorama.Back.RESET)
		sys.exit(10)		
	output_file_name = parse_result.output_file_name
	if parse_result.dso_type == '2':
		dso_type = 'waverunner'
	else:
		dso_type = 'wavejet'

else:
	print("Loading configuration file " + parse_result.ini_file)
	# Check for init file (load content and set default values where necessary), then print the used configuration as a check for the user
	try:
		config = configparser.ConfigParser()
		config.read(parse_result.ini_file)
				
		for group in config:
				
			if group == 'DSO':
				for key in config['DSO']:
					if key == 'dso_id':
						dso_id = config['DSO']['dso_id']
					elif key == 'dso_type':
						dso_type = config['DSO']['dso_type']
					elif key == 'channels':
						try:
							channels = rftools_misc.expand_mixrange(config['DSO']['channels'])
						except:
							print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: Invalid input parameter for the channels, exit."+ colorama.Style.NORMAL + colorama.Back.RESET)
							raise SystemExit
					elif key == 'number_of_segments':
						number_of_segments = int(float(config['DSO']['number_of_segments']))
					elif key == 'maximum_number_of_samples_per_segment':
						maximum_number_of_samples_per_segment = int(float(config['DSO']['maximum_number_of_samples_per_segment']))
					elif key == 'scope_vertical_range_volt_per_div':
						scope_vertical_range_volt_per_div = float(config['DSO']['scope_vertical_range_volt_per_div'])
					elif key == 'scope_horizontal_range_time_per_div':
						scope_horizontal_range_time_per_div = float(config['DSO']['scope_horizontal_range_time_per_div'])
					elif key == 'trigger':
						trigger = config['DSO']['trigger']
					elif key == 'trigger_channel':
						trigger_channel = int(float(config['DSO']['trigger_channel']))
					else:
						print(colorama.Back.YELLOW + colorama.Style.BRIGHT + "WARNING: Invalid key " + key + " detected and ignored." + colorama.Style.NORMAL + colorama.Back.RESET)
			
			elif group == 'OUTPUT':
				for key in config['OUTPUT']:
					if key == 'output_file_name':
						output_file_name = config['OUTPUT']['output_file_name']
					elif key == 'file_type':
						file_type = config['OUTPUT']['file_type']
			#else:
			#	print(colorama.Back.YELLOW + colorama.Style.BRIGHT + "WARNING: Invalid group " + group + " detected and ignored." + colorama.Style.NORMAL + colorama.Back.RESET)
		
	except BaseException as e:
		print(e)
		print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: Error while reading the configuration file, exit." + colorama.Style.NORMAL + colorama.Back.RESET)
		raise SystemExit

number_of_channels = len(channels)		

# Check parameters:
if dso_id == '':
	print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: No instrument ID has been specified, exit."+ colorama.Style.NORMAL + colorama.Back.RESET)
	raise SystemExit
if dso_type == 'wavejet':
	if number_of_segments > 1:
		number_of_segments = 1
		print(colorama.Back.YELLOW + colorama.Style.BRIGHT + "WARNING: Number of segments must be 1 for a WaveJet, using the default value of 1 segment."+ colorama.Style.NORMAL + colorama.Back.RESET)
if not dso_type in ['wavejet','waverunner']:
	print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: Invalid DSO type " + dso_type + ", exit."+ colorama.Style.NORMAL + colorama.Back.RESET)
	raise SystemExit
if not file_type in ['csv','bcf']:
	print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: Invalid file type " + file_type + ", exit."+ colorama.Style.NORMAL + colorama.Back.RESET)
	raise SystemExit
if file_type == 'csv' and not number_of_segments == 1:
	print(colorama.Back.YELLOW + colorama.Style.BRIGHT + "WARNING: CSV file type with more than 1 segment specified. Only the first segment will be written."+ colorama.Style.NORMAL + colorama.Back.RESET)

# Print values:
print("The following settings will be used:")
print(" DSO ID: " + dso_id)
print(" DSO type: " + dso_type)
print(" Channels: " + str(channels))
print(" Number of segments: " + str(number_of_segments))
print(" Max. number of samples per segment: " + str(maximum_number_of_samples_per_segment))
print(" Vertical range (V/div): " + str(scope_vertical_range_volt_per_div))
print(" Horizontal range (s/div): " + str(scope_horizontal_range_time_per_div))
print(" Trigger: " + trigger)
print(" Trigger channel: " + str(trigger_channel))
print(" Output file name: " + output_file_name)
print(" File type: " + file_type)


## Open connection to DSO:
if dso_type == 'wavejet':
	dso = rftools_remote.LeCroyWaveJet(dso_id)
	dso.connect(0)
elif dso_type == 'waverunner':
	dso = rftools_remote.LeCroyWaveRunner(dso_id)
	dso.connect(0)
if not dso.valid_connection:
	print(colorama.Back.RED + colorama.Style.BRIGHT + "Connection to DSO failed, exit."+ colorama.Style.NORMAL + colorama.Back.RESET)
	raise SystemExit
	
	
## Setup the scope:
#dso.setup(maximum_number_of_samples_per_segment, scope_horizontal_range_time_per_div, scope_vertical_range_volt_per_div, number_of_segments)


## Trigger if necessary:
if trigger == 'yes':
	print("Starting trigger.")
	dso.trigger_single(trigger_channel)
	if not dso.flag_valid_trigger:
		print(colorama.Back.RED + colorama.Style.BRIGHT + "Triggering failed, exit."+ colorama.Style.NORMAL + colorama.Back.RESET)
		raise SystemExit
	print("Trigger done.")
	
	
## Prepare output file
if file_type == 'bcf':
	if parse_result.data_type == '1':
		ci = [ (6, 6, 1, 't/s') ]
	else:
		ci = [ (6, 6, 0, 't/s') ]
	for channel in channels:
		if parse_result.data_type == '1':
			ci.append((103, 3, 1, 'Voltage channel ' + str(channel) + '/V'))
		else:		
			ci.append((103, 3, 0, 'Voltage channel ' + str(channel) + '/V'))
	fout = rftools_bcf.WriteBCF(output_file_name, time_stamp = time.time()*1e7, header_description_string='Created by DSO_GET', keys_string='device=' + str(dso.idn), column_information=ci,number_of_segments=number_of_segments)

elif file_type == 'csv':
	fout = rftools_csv.WriteCSV(output_file_name)
	
	
## Read the data of all specified channels
x = []
for cnt_ch in range(0,number_of_channels):
	dso.read(channels[cnt_ch])
	if not dso.flag_valid_data:
		print(colorama.Back.RED + colorama.Style.BRIGHT + "DSO_GET ERROR: reading data from DSO for channel " + str(channels[cnt_ch]) + " failed, exit."+ colorama.Style.NORMAL + colorama.Back.RESET)
		raise SystemExit
		
	if cnt_ch == 0:
		# Determine actual number of samples per segment
		number_of_samples_per_segment = dso.get_number_of_samples_per_segment()
		x = np.zeros((number_of_segments, number_of_samples_per_segment, number_of_channels+1))
		
	if dso_type == 'wavejet':
		x[0,:,cnt_ch+1] = dso.y
		if cnt_ch == 0:
			x[0,:,0] = dso.t
		
	elif dso_type == 'waverunner':
		for cnt_seg in range(0,number_of_segments):
			x[cnt_seg,:,cnt_ch+1] = dso.y[cnt_seg,:]
			if cnt_ch == 0:
				x[cnt_seg,:,0] = dso.t[cnt_seg,:]
				
				
# Write the data for each segment:
if file_type == 'bcf':
	if dso_type == 'wavejet':
		fout.write_segment(0, x[0,:,:])
		
	elif dso_type == 'waverunner':
		for cnt_seg in range(0,number_of_segments):
			fout.write_segment(dso.trigger_time[cnt_seg]*1e7, x[cnt_seg,:,:])
			
	fout.write_keys()

elif file_type == 'csv':
	tl = [6]				# type list
	ul = [6]				# unit list
	cl = ['Time/s']			# comment list
	for channel in channels:
		tl.append(103)
		ul.append(3)
		cl.append('Voltage channel ' + str(channel) + '/V')
	fout.write_column_file(type_list=tl, unit_list=ul, comment_list=cl, x=x[0,:,:], delimiter=', ')
	
	
# Success:
plt.show()
print(colorama.Back.GREEN + colorama.Style.BRIGHT + "DSO_GET: Done." + colorama.Style.NORMAL + colorama.Back.RESET)

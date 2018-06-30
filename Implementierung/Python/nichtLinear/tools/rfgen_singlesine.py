#!/usr/bin/python3
# STARFISH-PY: Software Tools for Accelerator RF Instrumentation via Command Shell using Python

version_string = 'Rev. 0.0.4, 03.01.2018'

#    STARFISH-PY, rfgen_singlesine: This tool generates a binary column file with a single sine pulse.
#    Copyright (C) 2017  GSI, Mohamed Ghanmi

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
import rftools_bcf
import sys, glob, argparse, colorama
import time



#Serves for Vizualisation
#import matplotlib.pyplot as plt


# Documentation data for Doxygen
## @package rfgen_singlesine.py
# This tool generates a binary column file (BCF) with a single sine pulse.
#
# This tool generates a single sine pulse according to the given parameters and then saves the result as a binary column file (BCF).
#
# \param[in] -h Help switch.
# \param[in] -o Name of output file.
# \param[in] -a Amplitude of the signal.
# \param[in] -n Number of samples of the generated signal.
# \param[in] -p Specifies the phase of the pulse.
# \param[in] --fpulse Frequency of the single sine pulse.
# \param[in] --frep Repetition frequency of the pulse.
# \param[in] --noise Noise level.
# \param[out] Integer number as error code (0: success, 1: general error, 10: error due to input parameters, 20: error while reading an input file, 21: input file has incorrect file format, 22: input file is empty, 30: error while writing the output file, 31: output file already exists)



def generate_singlesine(time = 0, samples_nb = 1000, rep_frequency = 10 , pulse_frequency = 50, amplitude = 1 , edge = 1, phase_offset = 0, noise = 0):
	"""This method generates a single sine pulse according to the given parameters.

	time: segment time.
	samples_nb: Number of samples of the generated signal
	rep_frequency: Repetition frequency of the pulse.
	pulse_frequency: Frequency of the single sine pulse.
	amplitude: Amplitude of the single sine pulse.
	edge: Gives whether the sine pulse has a rising or a falling edge.
	phase_offset: Phase offset of the single sine pulse.
	noise: Noise level.
    """

	if edge not in [0,1]:
		print(colorama.Back.RED + colorama.Style.BRIGHT + "ERROR: invalid phase (either 0 for a rising or a 1 for a falling edge) , exit."+ colorama.Style.NORMAL + colorama.Back.RESET)
		# Return code for error (empty input file):
		sys.exit(10)


	#Creating empty lists for t and y
	t = np.zeros(samples_nb)

	if noise == 0:
		y = np.zeros(samples_nb)
	else:
		y = np.random.normal(0, noise, samples_nb)

	#Determining the interval limits of t
	t_limit =1/float(rep_frequency*2)

	#Updating the t interval
	t = np.arange(-samples_nb/2,samples_nb/2)/float(samples_nb*rep_frequency) + 1/float(samples_nb*rep_frequency)


	#calculating the time_shift
	#delta_t = phase_offset/(2*np.pi*pulse_frequency)
	delta_t = phase_offset/(2*np.pi*rep_frequency)

	#Setting the pulse amplitude
	a_pulse = amplitude
	if edge == 1:
		a_pulse *= -1

	#Calculating the pulse limits
	p_limit = 1/float(2*pulse_frequency)
	p_interval = list ([-p_limit,p_limit])


	for n in range (0,len(t)) :
		if (t[n] + delta_t) > p_interval[0] and (t[n] + delta_t) <= p_interval[1]:
			y[n] += a_pulse * np.sin(2*np.pi*pulse_frequency*(t[n]+delta_t))



	#plt.plot(t,y)
	#plt.show()

	result = {}
	result ['time'] = time
	result ['t'] = t
	result ['y'] = y

	return result

if __name__ == "__main__":

	# Initialization of colored text output:
	colorama.init()

	copyright_message = "STARFISH-PY, RFGEN_SINGLESINE  Copyright (C) 2017  M.Ghanmi This program comes with ABSOLUTELY NO WARRANTY; This is free software, and you are welcome to redistribute it under certain conditions; see 'LICENCE' for details. "

	long_description = "This tool generates a binary column file with a single sine pulse with a predefined pulse frequency fpulse and repetition frequency frep. The time axis of the generated signal starts at zero and stops at 1/ frep. The single sine pulse is located in the middle of the interval."

	# Parse the command line arguments:
	parser = argparse.ArgumentParser(description= copyright_message +long_description+'Version:' + version_string + '.')

	parser.add_argument('-o', action="store", dest="output_file", required=True, help='Name of output file.')
	parser.add_argument('-a', action="store", dest="amplitude", default='1', help='Amplitude of the signal, default value is 1.')
	parser.add_argument('-n', action="store", dest="samples_nb", default='1000', help='Number of samples of the generated signal, default is 1000.')
	parser.add_argument('-p', action="store", dest="phase", default='0', help='Specifies the phase of the pulse: 0 = rising edge, 1 = falling edge, default is 0.')
	parser.add_argument('--fpulse', action="store", dest="sine_frequency", required=True, help='Frequency of the single sine pulse in Hertz.')
	parser.add_argument('--frep', action="store", dest="rep_frequency", required=True, help='Repetition frequency of the pulse in Hertz.')
	parser.add_argument('--noise', action="store", dest="noise", default='0', help='Noise level (standard deviation of Gaussian noise), default is 0.')
	parse_result = parser.parse_args(sys.argv[1:])

	print(colorama.Back.GREEN + colorama.Style.BRIGHT + "RFGEN_SINGLESINE: Start." + colorama.Style.NORMAL + colorama.Back.RESET)

	# Check parameters:
	output_string = parse_result.output_file

	if not output_string[-4:] == ".bcf":
		output_string += ".bcf"



	amplitude = float(parse_result.amplitude)
	samples_nb = int (parse_result.samples_nb)
	phase = int(parse_result.phase)
	sine_frequency = float(parse_result.sine_frequency)
	rep_frequency = float(parse_result.rep_frequency)
	noise = float(parse_result.noise)

	#Check whether the number of sampling points is reasonable
	if samples_nb < 1:
		print(colorama.Back.YELLOW + colorama.Style.BRIGHT + "RFGEN_SINGLESINE: Number of requested sample points is less than 1, nothing to do, exit." + colorama.Style.NORMAL + colorama.Back.RESET)
		sys.exit(10)

	if phase not in [0,1]:
		print(colorama.Back.YELLOW + colorama.Style.BRIGHT + "RFGEN_SINGLESINE: Unvalid phase, should be either 0 or 1, nothing to do, exit." + colorama.Style.NORMAL + colorama.Back.RESET)
		sys.exit(10)

	if rep_frequency > sine_frequency:
		print(colorama.Back.YELLOW + colorama.Style.BRIGHT + "RFGEN_SINGLESINE: Repetition frequency should not be greater than the sine one, nothing to do, exit." + colorama.Style.NORMAL + colorama.Back.RESET)
		sys.exit(10)

	# Single sine pulse generation
	signal = generate_singlesine(time = 0, samples_nb = samples_nb, rep_frequency = rep_frequency , pulse_frequency = sine_frequency, amplitude = amplitude  , edge = phase, phase_offset = 0, noise = noise)

	#Write the BCF output file

	# This is the current time in steps of 100 nanoseconds (cf. the document with the definition of the BCF file format):
	time_stamp = time.time()*1e7
	header_description = 'Generated by RFGEN_SINGLESINE'
	keys_string = 'device=RFGEN_SINGLESINE'

	column_information = [ (6, 6, 1, 't/s'), (103, 3, 1, 'y/V') ]
	# This calls the constructor of the WriteBCF class:
	outfile = rftools_bcf.WriteBCF(output_string, time_stamp, header_description, keys_string, column_information)

	# First write the header:
	outfile.write_header()

	# Now write the segments:
	relative_time = 0
	x = np.column_stack((signal['t'],signal['y']))
	outfile.write_segment(relative_time*1e7, x)

	# Write the keys, this finishes the file:
	outfile.write_keys()

	#Success
	print("Output file " + output_string + " has been written.")
	print(colorama.Back.GREEN + colorama.Style.BRIGHT + "\nRFGEN_SINGLESINE: Done." + colorama.Style.NORMAL + colorama.Back.RESET)
	# Return code 0 (success):
	sys.exit(0)

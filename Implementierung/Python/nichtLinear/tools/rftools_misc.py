## @package RFTOOLS_MISC
# Python package with routines for RF data analysis.
# 
import numpy as np

version_string = 'Rev. 0.1.8, 01.10.2017'

# History
# Rev. 0.1.4: Removed bug in get_key_value ("ind+1 > len(text_string)" instead of ">=")

## Function for expansion of number range such as 1-3,6,8-10
# 
# Taken from http://stackoverflow.com/questions/18759512/expand-a-range-which-looks-like-1-3-6-8-10-to-1-2-3-6-8-9-10
# @param s String containing a number range (e.g. 1-3,6,8-10)
# @return 
def expand_mixrange(s):
	r = []
	for i in s.split(','):
		if '-' not in i:
			r.append(int(i))
		else:
			l,h = map(int, i.split('-'))
			r += range(l,h+1)
	return r


## Function for expansion of number range such as 1-3,6,8-10. It also supports a stepsize and reverse ranges such as 3-1,7-4
# 
# @param s String containing a number range (e.g. 1-3,6,8-10)
# @return 
def expand_mixrange_with_stepsize(range_string, stepsize):
	r = []
	for i in range_string.split(','):
		if '-' not in i:
			r.append(int(float(i)))
		else:
			l,h = map(float, i.split('-'))
			if h >= l:
				if stepsize > 0:
					temp = np.arange(int(l), int(h)+1, stepsize)
				else:
					temp = np.arange(int(h), int(l)-1, stepsize)
			else:
				if stepsize > 0:
					temp = np.arange(int(l), int(h)-1, -stepsize)
				else:
					temp = np.arange(int(h), int(l)+1, -stepsize)
			r += list(temp)
	return r


## Function for automatic unit conversion
#
# The most convenient unit string and conversion factor is returned. This should work for most plots.
def auto_unit_conversion(unit_value, unit_string, max_value, use_degree=False):
	if max_value == 0:
		return 1, unit_string

	magn_list = np.array([1e-12, 1e-9, 1e-6, 1e-3, 1, 1e3, 1e6, 1e9])
	magn_inv_list = np.array([1e12, 1e9, 1e6, 1e3, 1, 1e-3, 1e-6, 1e-9])
	magn_strings = ['p', 'n', '$\mu$', 'm', '', 'k', 'M', 'G']
	# Find most appropriate magnitude (item of ratio between maximum value and magnitude list with absolute value closest to 100):
	idx = (np.abs(np.abs(max_value/magn_list) - 100)).argmin()
	
	# Radian:
	if unit_value == 2:
		if use_degree:
			return 180/np.pi, unit_string.split("/")[0]+"/Degree" #'Phase/Degree'
		else:
			return 1, unit_string
	else:
		unit_string_list = unit_string.split("/")
		if len(unit_string_list) > 1:
			return 1/magn_list[idx], unit_string_list[0]+"/"+magn_strings[idx]+unit_string_list[1]
			
		else:
		
			if unit_value == 1:
				return 1/magn_list[idx], unit_string_list[0]+"/"+magn_strings[idx]+"T"
			elif unit_value == 3:
				return 1/magn_list[idx], unit_string_list[0]+"/"+magn_strings[idx]+"V"
			elif unit_value == 4:
				return 1/magn_list[idx], unit_string_list[0]+"/"+magn_strings[idx]+"Hz"
			elif unit_value == 6:
				return 1/magn_list[idx], unit_string_list[0]+"/"+magn_strings[idx]+"s"
			elif magn_inv_list[idx] == 1:
				return 1, unit_string_list[0]
			else: 
				return 1/magn_list[idx], unit_string_list[0]+"  *  "+str(magn_inv_list[idx])+""
				#return 1/magn_list[idx], magn_strings[idx]
						
	
	# Tesla:
	#if unit_value == 1:
	#	return 1/magn_list[idx], 'B/'+magn_strings[idx]+'T'	
	# Radian:
	#if unit_value == 2:
	#	if use_degree:
			#return np.rad2deg(unit_value), 'Phase/Degree'
	#		return 180/np.pi, unit_string.split("/")[0]+"/Degree" #'Phase/Degree'
		#else:
			#return 1/magn_list[idx], 'Phase/'+magn_strings[idx]+'rad'
	# Volt:
	#if unit_value == 3:
	#	return 1/magn_list[idx], 'Amplitude/'+magn_strings[idx]+'V'
	# Hertz:
	#if unit_value == 4:
	#	return 1/magn_list[idx], 'f/'+magn_strings[idx]+'Hz'
	# Seconds:
	#if unit_value == 6:
	#	return 1/magn_list[idx], 't/'+magn_strings[idx]+'s'
	#else:
	#	return 1, unit_string

	
## Search for a specific key in a string
#  Returns the value of the key if the key is found, or else "" (for strings) or np.nan (for int or float) if it is not found.
#  @param self			The object pointer 
#  @param text_string	String containing keys
#  @param key_string	String, identifier of the key (key name)
#  @param var_type	Expected type of key value: 'string', 'int', 'float'
def get_key_value(text_string, key_string, var_type):
	if not(key_string in text_string): # key not found
		if var_type == 'string':
			return ''
		else:
			return np.nan
	ind = text_string.find(key_string) + len(key_string) + 1
	value = ""
	if ind+1 > len(text_string):
		return value
	elif text_string[ind] == "'": # This is a string with leading and trailing quotation marks
		ind2 = text_string[ind+1:].find("'") # Find the trailing quotation mark
		if ind2 == -1 or ind+ind2+2 > len(text_string):
			print("RFTOOLS_CSV, get_key_value() ERROR: key string " + key_string + " seems to be corrupted. A string with a leading quotation mark but without trailing quotation mark has been found. The key could not be read and is ignored.")
			return ""
		#print("Key detected: " + text_string[ind:ind+ind2+2])
		return text_string[ind:ind+ind2+2]
		#while ind < len(text_string):
		#	value += text_string[ind]
		#	ind +=1
		#	if text_string[ind] == "'":
		#		value += "'";
		#		break	
	else:
		while ind < len(text_string):
			if text_string[ind] == " ":
				break
			value += text_string[ind]
			ind += 1
	if var_type == 'string':
		return value
	elif var_type == 'int':
		try:
			return int(value)
		except:
			print('ERROR (ReadCSV.get_key_value()): key value is not convertable to int: ' + value)	
			return np.nan
	elif var_type == 'float':
		try:
			return float(value)
		except:
			print('ERROR (ReadCSV.get_key_value()): key value is not convertable to int: ' + value)	
			return np.nan
	else:
		print('ERROR (ReadCSV.get_key_value()): invalid type of key: ' + str(var_type))
		return np.nan

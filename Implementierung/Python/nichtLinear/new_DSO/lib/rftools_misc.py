## @package RFTOOLS_MISC
# Python package with routines for RF data analysis.
# GSI, D. Lens, 2016-2018
import numpy as np

version_string = 'Rev. 0.1.10, 12.05.2018'

# History
# Rev. 0.1.9: 
# - New functions "type_string" and "unit_string"
# Rev. 0.1.4: 
# - Removed bug in get_key_value ("ind+1 > len(text_string)" instead of ">=")


## Returns the string of a numeric type value
def type_string(type_value):
	if type_value == 0:
		return 'unspecified'
	elif type_value == 1:
		return 'B field'
	elif type_value == 2:
		return 'synchronous phase'
	elif type_value == 3:
		return 'RF amplitude'
	elif type_value == 4:
		return 'RF frequency'
	elif type_value == 5:
		return 'relativistic gamma'
	elif type_value == 6:
		return 'time'
	elif type_value == 7:
		return 'revolution frequency'
	elif type_value == 8:
		return 'RF phase'
	elif type_value == 9:
		return 'synchrotron frequency'
	elif type_value == 50:
		return 'beam current'
	elif type_value == 103:
		return 'voltage'
	elif type_value == 104:
		return 'frequency'
	elif type_value == 105:
		return 'harmonic number'
	elif type_value == 106:
		return 'impedance'
	elif type_value == 107:
		return 'phase'
	elif type_value == 108:
		return 'current'
	elif type_value == 109:
		return 'temperature'
	elif type_value == 200:
		return 'time stamp'
	else:
		return 'not defined'
		
		
## Returns the string of a numeric unit value
def unit_string(unit_value):
	if unit_value == 0:
		return 'unspecified'
	elif unit_value == 1:
		return 'T'
	elif unit_value == 2:
		return 'rad'
	elif unit_value == 3:
		return 'V'
	elif unit_value == 4:
		return 'Hz'
	elif unit_value == 5:
		return 'dimensionless'
	elif unit_value == 6:
		return 's'
	elif unit_value == 50:
		return 'degree Celcius'
	elif unit_value == 60:
		return 'Ohm'
	elif unit_value == 61:
		return 'A'
	elif unit_value == 62:
		return 'a.u.'
	elif unit_value == 200:
		return 'system ticks'
	else:
		return 'not defined'
	

## Function for expansion of number range such as 1-3,6,8-10
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

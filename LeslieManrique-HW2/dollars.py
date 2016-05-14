import re
import sys

source = sys.argv[1] 
output = sys.argv[2] 

try:
	#open a text file for reading
	f = open(source,'r')
	lines  = f.read() 

	indexes = []
	match = []

	#for m in re.finditer(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})',lines):
	#for m in re.finditer(r'$[0-9]+(\.[0-9][0-9])?',lines):	
	#for m in re.finditer(r'^\$?(\d*(\.\d\d?)?|\d+)$',lines):
	#for m in re.finditer(r'\$?[\d,]*\d,\d{3}\.\d{2}',lines):
	for m in re.finditer(r'(\$?(?:(?:\d{1,3}(?:,+\d{3}){1,})|\d{4,})\.\d{2})',lines):
	#for m in re.finditer(r'\$[0-9.]+',lines):	
		s = m.start()
		e = m.end()
		index = [s,e]
		indexes.append(index)
		match.append(lines[s:e])

	for m in re.finditer(r'(([Oo]ne)|([Tt]wo)|([Tt]hree)|([Ff]our)|([Ff]ive)|([Ss]ix)|([Ss]even)|([eE]ight)|([nN]ine))+ ([hH]undred)?([tT]housand)?([mM]illion)?([bB]illion)? ([dD]ollars?)',lines):
		s = m.start()
		e = m.end()
		index = [s,e]
		indexes.append(index)
		match.append(lines[s:e])

	for m in re.finditer(r'\$[0-9.]+',lines):	
		s = m.start()
		e = m.end()
		index = [s,e]
		indexes.append(index)
		match.append(lines[s:e])
	new_lines = lines
	print(match)
	count = 0
	for i in indexes:
		new_lines = new_lines[:i[0]+count] + '[' + new_lines[i[0]+count:i[1]+count] + ']' + new_lines[i[1]+count:]
		count+=2

	#OUTPUT FILE
	f = open(output,'w')
	for line in new_lines:
		f.write(line) 

	f.close() 

except IOError:
	print("File Not Found")
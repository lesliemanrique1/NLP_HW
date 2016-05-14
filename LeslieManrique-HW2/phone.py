import re
import sys

source = sys.argv[1] 
output = sys.argv[2] 

try:
	#open a text file for reading
	f = open(source,'r')
	lines  = f.read() 

	indexes = []

	for m in re.finditer(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})',lines):
		s = m.start()
		e = m.end()
		index = [s,e]
		indexes.append(index)

	new_lines = lines

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
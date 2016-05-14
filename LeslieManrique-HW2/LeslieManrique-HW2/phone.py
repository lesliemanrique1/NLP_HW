#Leslie Manrique
#HW_2 
#Due: 2/10/2016 
#Description:   This is 2/2 program scripts for assignment 2.
#               Identifies phone numbersfrom a given source file.
#               Source file is identified by first command line argument. 
#               Writes output to a separate file - expression matches phone.txt
#		Rewrites the original file to include brackets around expressions
#		as indicated by second command line argument

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
	for m in re.finditer(r'(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})',lines):
		s = m.start()
		e = m.end()
		index = [s,e]
		indexes.append(index)
		match.append(lines[s:e])

	new_lines = lines

	count = 0
	for i in indexes:
		new_lines = new_lines[:i[0]+count] + '[' + new_lines[i[0]+count:i[1]+count] + ']' + new_lines[i[1]+count:]
		count+=2

	#OUTPUT FILE
	f = open(output,'w')
	g = open("phone.txt",'w')
	for line in new_lines:
		f.write(line) 

	for item in match:
		g.write(item)
		g.write("\n")
	f.close() 
	g.close()

except IOError:
	print("File Not Found")

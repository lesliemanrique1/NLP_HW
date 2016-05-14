#Leslie Manrique
#HW_2 
#Due: 2/10/2016 
#Description:	This is 2/2 program scripts for assignment 2.
#		Identifies telephone numbers from a given source file.
#		Source file is identified by first command line argument. 
#		Writes output to a separate file as indicated by second 
#		command line argument. 

import nltk 
import re 
import sys

#takes in two command line arguments first being the source file and 
#second being the file to write to 
source = sys.argv[1] 
output = sys.argv[2] 


p1matches = []  
p2matches = [] 
p3matches = [] 
p4matches = []
p5matches = [] 
try:
	#open a text file for reading
	f = open(source,'r')
	lines  = f.read() 
	f.close()
	#print(lines)
	#Pattern 1
		#xxx-xxx-xxxx
		#xxx.xxx.xxxx 
	
	#Pattern 2
		#xxx-xxxx
		#xxx.xxxx
	#Pattern 3
		#x-xxx-xxx-xxxx
		#x.xxx.xxx.xxxx
	
	#Pattern 4
		#xxxxxxxxxxx
		#xxxxxxxxxx
		#xxxxxxx
	#Pattern 5
		#(xxx) xxx-xxxx
		#(xxx) xxx.xxxx
		#(xxx) xxx xxxx

	indexes = [] 
	dmatches = [] 
	for m in re.finditer(r'\b[0-9]{3}[-\.][0-9]{3}[-\.][0-9]{4}\b',lines):
		s = m.start()
		e = m.end()
		index = [s,e] 
		indexes.append(index) 
		print(lines[s:e]) 
		print("\n") 
		dmatches.append(lines[s:e]) 	
	for m in re.finditer(r'\b[0-9][-\.][0-9]{3}[-\.][0-9]{3}[-\.][0-9]{4}\b',lines):
		s=m.start()
		e=m.end()
		index = [s,e]
		indexes.append(index) 
		print(lines[s:e])
		dmatches.append(lines[s:e])
	for m in re.finditer(r'\b[0-9]{3}[-\.][0-9]{4}\b',lines):
		s=m.start()
		e=m.end()
		index = [s,e]
		indexes.append(index)
		print(lines[s:e])
		dmatches.append(lines[s:e])
	for m in re.finditer(r'\b[0-9]{7-11}\b',lines):
	#for m in re.finditer(r'\b([0-9]{7}|[0-9]{10}|[0-9]{11})\b',lines):
		s=m.start()
		m=m.end()
		index = [s,e]
		indexes.append(index)
		print(lines[s:e])
		dmatches.append(lines[s:e])
	#for m in re.finditer(r'\b\([0-9]{3}\)[\s\S][0-9]{3}[-\.\s ][0-9]{4}\b',lines):
		
	for m in re.finditer(r'\([0-9]{2,4}\)[\s]* ([0-9]{2,4})-([0-9]{2,4})\b',lines):	
		s=m.start()
		m=m.end()
		index=[s,e]
		indexes.append(index) 
		print(lines[s:e]) 
		dmatches.append(lines[s:e])
	
	print(dmatches)
	new_lines=lines

	count  = 0; 
	for i in indexes:
		new_lines = new_lines[:i[0]+count] + '[' + new_lines[i[0]+count:i[1]+count] + ']'+new_lines[i[1]+count:]
		count+=2 
		
	
	
	#OUTPUT FILE
	f = open(output,'w')
	for line in lines:
		f.write(line) 
	f.close() 

except IOError:
	print("File Not Found") 

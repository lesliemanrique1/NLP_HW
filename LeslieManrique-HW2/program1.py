#Leslie Manrique
#HW_2 
#Due: 2/10/2016 
#Description:	This is 1/2 program scripts for assignment 2.
#		Identifies dollar amounts from a given source file.
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
 
try:
	#open a text file for reading
	f = open(source,'r')
	lines = f.read() 
	regex = re.compile(r'\b$[0-9]+(\.[0-9][0-9])?\b',lines)
	result = regex.match(lines)
	print(result)
	#regex = re.compile(r'^\$?([0-9]*([0-9]\.?|\.[0-9]{1,2}))$')
	#pattern = re.compile(r'\b^$?([0-9]
	#money = re.compile('|'.join([r'^\$?(\d*\.\d{1,2})$',r'^\$?(\d+)$',r'^\$(\d+\.?)$',])) 
	
	#go through the text file and match regexp 
	#case 1 - sample like "One billion dollars" 
	#case 2 - sample like "One billion dollars and seventy five cents
	#case 3 - sample like "1,000,000" or "1,000,000 dollars" 
	#case 4 - sample like "$1,000,000" 
	#case 5 - sample like "$1000000" 
	#case 6 - sample like 

	
	
except IOError:
	print("File Not Found") 

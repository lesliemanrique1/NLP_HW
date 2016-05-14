{\rtf1\ansi\ansicpg1252\cocoartf1404\cocoasubrtf340
{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
\margl1440\margr1440\vieww10800\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 #Homework Number 4 \
\
###Includes Two Files : \
viterbi_run.py                Runs the viterbi algorithm \
viterbi.py                    Library of functions\
\
###To run this file: \
\
	python viterbi_run.py trainingfile  developmentfile runfile \
\
trainingfile - file used as training corpus WSJ_02-21.pos\
\
developmentfile - file used as development set WSJ_24.pos\
\
runfile - file to run system on \
\
\
This program produces a file called ***Leslie_Manrique_WSJ_23.pos***. \
\
### Implementation \
I\
For this assignment, I implemented a bigram systems, as show in Chapter 5 of Martin and Jurafsky book. \
The training file and development file are merged to create a larger file that will be outputed as merged.txt. \
\
###OOV Words\
\
The hardest part was handing OOV words. I accomplished this via the following code: \
\
\
  	def OOV_tag(word,index,pos_keys):\
		OOV_pos = [] \
	\
		#if there's a hyphen , return JJ\
		if '-' in word:\
			if 'JJ' not in OOV_pos: \
				OOV_pos.append('JJ')\
	\
		#if word ends with able, return JJ \
		if 'able' in word:\
			if 'JJ' not in OOV_pos: \
				OOV_pos.append('JJ') \
			\
	\
		#if word is numnerical, return CD \
		if unicode(word).isnumeric():\
			#print(word)\
			if 'CD' not in OOV_pos: \
				OOV_pos.append('CD') \
		if float(isfloat(word)):\
			#print(word)\
			#print(float(word)) \
			if 'CD' not in OOV_pos:\
				OOV_pos.append('CD') \
		#if it starts with an uppercase letter and is not found at the beginning of the sentence AND end with an S return NNPS \
		if word[0].isupper() and index > 0 and word[-1] == 's':\
			if 'NNPS' not in OOV_pos: \
				OOV_pos.append("NNPS") \
	\
		#if it starts with an uppercase letter and is not found at the beginning of the sentence\
		#return NNP\
		if word[0].isupper() and index > 0:\
			if 'JJ' not in OOV_pos: \
				OOV_pos.append("NNP") \
	\
		#if it ends with an s then return NNS \
		if word[-1] == 's':\
			if 'NNS' not in OOV_pos: \
				OOV_pos.append("NNS")  \
	\
		#if it ends with ing, return VBG\
		if word[-3:] == 'ing':\
			if 'VBG' not in OOV_pos: \
				OOV_pos.append("VBG") \
			if 'VB' not in OOV_pos:\
				OOV_pos.append("VB") \
		#if it ends with ed, return VBD \
		if word[-2:] == 'ed':\
			if 'VBD' not in OOV_pos: \
				OOV_pos.append('VBD') \
		\
		#if it ends with ly return RB \
		if word[-2:] == 'ly':\
			if 'RB' not in OOV_pos: \
				OOV_pos.append('RB')\
		#if it ends with er return JJR\
		if word[-2:] == 'er':\
			if 'JJR' not in OOV_pos: \
				OOV_pos.append('JJR')  \
		#if it ends with est return JJS \
		if word[-3:] == 'est':\
			if 'JJS' not in OOV_pos: \
				OOV_pos.append('JJS')  \
		if len(OOV_pos) == 0: \
			if 'N' not in OOV_pos: \
				OOV_pos.append('NN')\
		return OOV_pos \
\
Default an OOV word is likely to be a nount. As each if statement is checked, when true is returned, it will add\
the part of speech to a list of parts of speeches. \
\
The likelihood for out of vocabulary words were automatically set to ***1/100K***\
\
###Problems\
\
I ran into problems with this project. After finishing up my code, there were some transitions that\
were not found in my prior probabilities table. Therefore when the part of speech is selected, there was a gap in my Viterbi lookup\
table. So, when finding the path, the path was set to default 0, which made the words be tagged to 'S' which i used to signify\
the start of a sentence. \
\
The algorithm also takes a bit to run, but usually 60 to 80 seconds. \
\
All in all, from my tests using ***score.py*** I was able to achieve over 95% accuracy when tagging the file WSJ_24.words.\
\
}
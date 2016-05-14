import numpy 
import csv
import re 
#NOTE:
#
#		Find a new way to form corpus list 
#reads from training file 
#returns a an array of sentence arrays made of tuples (Word,POS)
#@param filename 	name of file to read
#@return array 		list of sentence lists of tuples 
def corpus_list(filename):
    
    tf = open(filename , 'r')

    sent_cond = True 
    sentence = []
    array = []
    count = 0
    for line in tf:
        l = line.split()
	if (len(l) == 0):
		array.append(sentence) 
		sentence = [] 
	else:
		tags = (l[0],l[1]) 
		sentence.append(tags)
  
    tf.close()
    return array 

#returns a dictionary of the part of speech tag with number of occurences
#@param filename	file to read from 
#@return dic		dictionary 
def corpus_dictionary(filename): 
	training = filename 
	tf = open(training,'r') 
	dic = {}
	for line in tf:
		l = line.split()
		if(len(l) == 2):
			#check if key is existing 
			if l[1] in dic:
				dic[l[1]]+=1 
			else:
				dic[l[1]] = 1
	return dic 




#returns a list of dictionary key
#@param	dictionary	dictionary
#@return pos_list	list of dictionary keys
def key_list(dic):
	list_  = list(dic.keys()) 
	return list_


#prints matrix and row and column headers to a csv file titles 'prior_probabilities.csv'
#@param matrix          the matrix or 2d list that includes the number of times each 
#                       transition occurs in corpus
#@param list_1		column headers
#@param list_2		row headers
def print_csv(filename,matrix,list_1,list_2):
	f = open(filename,'wb')
	with f as out:
		writer = csv.writer(out) 
		writer.writerow(['']+list_1)
		j = 0
		for i in matrix:
			writer.writerow([list_2[j]] + map(lambda num:num,i))
			j+=1
		
#according to the corpus, counts how many times a transition occurs in a matrix
#@param sentence	list of tuples ('word','part of speech') 
#@param matrix          the matrix or 2d list that includes the number of times each 
#                       transition occurs in corpus
#@param list_1		column header 
#@param list_2		row header 
def helper_transition(sentence,matrix,list_1,list_2):
	this_sentence = [('','S')] + sentence + [('','E')]
	#print this_sentence
	#for i in sentence:
	for i in range(len(this_sentence)-1):
		current = this_sentence[i][1]
		row = list_2.index(current) 
		following = this_sentence[i+1][1]
		column = list_1.index(following) 
		matrix[row][column]+=1 

#calculates the prior probabilities 
#@param corpus_list	list of sentences in corpus with words as tuples 
#@param matrix		the matrix or 2d list that includes the number of times each 
#			transition occurs in corpus
#@param dic		dictionary of corpus pos : number of times pos occurs
#@param list_2 		the list that contains the pos tag which are the row headers 
#@return None		no return value; void 
def calculate_prior_probabilities(corpus_list,matrix,dic,list_2):
	for i in range(len(matrix)):
		if i > 0:
			for j in range(len(matrix[i])):
					key = list_2[i]
					matrix[i,j] = matrix[i,j]/dic[key] 
		else:
			dividend = len(corpus_list)
			for j in range(len(matrix[i])):
				matrix[i,j] = matrix[i,j]/dividend 	

#creates the transition table  
#@param corpus_list	list of sentences with words as tuples 
#@return table		returns prior probabilities transition table 
def transition_table(dic,corpus_list):
	ls = key_list(dic) 

	list_1 =  ls + ['E'] #columns 
	list_2 = ['S'] + ls #rows
	#creates a matrix with indexes initialized to 0 using numpy 
	table = numpy.zeros(shape = (len(list_2),len(list_1)))
	#add values to table sentence by sentence
	for i in corpus_list:
		#call to helper function 
		helper_transition(i,table,list_1,list_2)

	#calculate prior probabilities 
	calculate_prior_probabilities(corpus_list,table,dic,list_2) 
	#prints prior probabilities table to csv file 
#	print_csv('prior_probabilities.csv',table,list_1,list_2)  
	return table




#----------------------likelihood table----------------------------------#

#creates a dictionary of the different words in the corpus 
#@param corpus_list	list of words and part of speeches 
#@param keys		column header 
#@return dic		dictionary 
def word_dic(corpus_list, keys):
	dic = {} 
	#print(keys)
	for i in corpus_list:
		for j in i:
			word = j[0].lower() 
			pos = j[1]
			#create dictionary 
			if word in dic:
				index = keys.index(pos) 
				dic[word][index] += 1  
			else:
				#create dictionary element first
				dic[word] = [0]*len(keys) 
				index = keys.index(pos)
				dic[word][index] +=1 
				
	#print(dic)
	return dic 

 

#calculates word frequencies and outputs table into csv file named likelihood.csv 
#@param pos_dic		dictionary of part of speech and their occurences
#@param word_dic	dictionary of words and their occurences of each port of speech 
#@return table		the likelihood matrix
def word_freq(pos_dic,word_dic):
	#get list of keys in word_dic 
	word_keys = key_list(word_dic) 
	pos_keys = key_list(pos_dic) 
	table = numpy.zeros(shape = (len(word_keys),len(pos_keys)))  
	count = 0 
	for key in word_dic:
		for i in range(len(word_dic[key])):	
			#print(word_dic[key][i]) 
			pos_occurences = pos_dic[pos_keys[i]] 
			#print(pos_occurences) 
			#pos_occurences = pos_dic[i]
			#print(pos_occurences)
			#print(word_dic[key][i]) 
			table[count,i] = float(word_dic[key][i])/float(pos_occurences) 
			
		count+=1 
	#print_csv('likelihood.csv',table,pos_keys,word_keys)

	return table


#-----------------Viterbi Algorithm------------
#Creates an Array of sentences 
def corpus_list_2(filename): 
	tf = open(filename,'r') 
	#sent_cond = True 
	sentence = [] 
	array = []
	for line in tf:
		l = line.split()
		if(len(l) == 0):
			array.append(sentence) 
			sentence = []
		else:
			tags = (l[0]) 
			sentence.append(tags) 

		
		
	tf.close()

	return array

#return OOV list of possabilities 

def isfloat(string):
	condition = False 
	try:
		float(string)
		condition = True   
	except ValueError:
		condition = False
	
	if condition == False: 
		try:
			float(string.replace(',','')) 
			condition = True 
		except ValueError:
			condition = False 
	return condition 


def OOV_tag(word,index,pos_keys):
	OOV_pos = [] 

	#if there's a hyphen , return JJ
	if '-' in word:
		if 'JJ' not in OOV_pos: 
			OOV_pos.append('JJ')

	#if word ends with able, return JJ 
	if 'able' in word:
		if 'JJ' not in OOV_pos: 
			OOV_pos.append('JJ') 
		

	#if word is numnerical, return CD 
	if unicode(word).isnumeric():
		#print(word)
		if 'CD' not in OOV_pos: 
			OOV_pos.append('CD') 
	if float(isfloat(word)):
		#print(word)
		#print(float(word)) 
		if 'CD' not in OOV_pos:
			OOV_pos.append('CD') 

	#if it starts with an uppercase letter and is not found at the beginning of the sentence AND end with an S return NNPS 
	if word[0].isupper() and index > 0 and word[-1] == 's':
		if 'NNPS' not in OOV_pos: 
			OOV_pos.append("NNPS") 

	#if it starts with an uppercase letter and is not found at the beginning of the sentence
	#return NNP
	if word[0].isupper() and index > 0:
		if 'JJ' not in OOV_pos: 
			OOV_pos.append("NNP") 

	#if it ends with an s then return NNS 
	if word[-1] == 's':
		if 'NNS' not in OOV_pos: 
			OOV_pos.append("NNS")  

	#if it ends with ing, return VBG
	if word[-3:] == 'ing':
		if 'VBG' not in OOV_pos: 
			OOV_pos.append("VBG") 
		if 'VB' not in OOV_pos:
			OOV_pos.append("VB") 
	#if it ends with ed, return VBD 
	if word[-2:] == 'ed':
		if 'VBD' not in OOV_pos: 
			OOV_pos.append('VBD') 
	
	#if it ends with ly return RB 
	if word[-2:] == 'ly':
		if 'RB' not in OOV_pos: 
			OOV_pos.append('RB')
	#if it ends with er return JJR
	if word[-2:] == 'er':
		if 'JJR' not in OOV_pos: 
			OOV_pos.append('JJR')  
	#if it ends with est return JJS 
	if word[-3:] == 'est':
		if 'JJS' not in OOV_pos: 
			OOV_pos.append('JJS')  
	if len(OOV_pos) == 0: 
		if 'N' not in OOV_pos: 
			OOV_pos.append('NN')
	
#	print("word: ",word," list: ", OOV_pos) 
	return OOV_pos 

#finds parts of speeches for all words in sentence using corpus and OOV_tag function 
def sentence_tag(sentence,pos_keys, word_keys, likelihood_table):  
	#first find the parts of speeches 
	dic = {} 
	i = 0 
	#print(sentence)
	for word in sentence:
	 
		#find row index in likelihood table
		pos_list =[] 
		try:
			word_index = word_keys.index(word.lower()) 
		except ValueError:
			word_index = -1

		if word_index > -1: 
			for j in range(len(likelihood_table[word_index])):
				if likelihood_table[word_index][j] > 0:
					pos_list.append(pos_keys[j]) 
		else:
			pos_list = OOV_tag(word,i,pos_keys) 
		dic[i] = pos_list 

		i+=1 

	return dic

#gets all the unique part of speech tags from the sentece x part of speech dictionary 

def sentence_pos(dic):
	pos_list = [] 
	for key in dic: 
		for val in dic[key]:
			if val not in pos_list:
				pos_list.append(val)
	return pos_list
#def sentence_tag_transition(sentence,pos_keys,pp_table)


def transition_probabilities(dic,pos_list,transition_table,pos_keys):
	rows = ['S'] + pos_list 
	columns = pos_list + ['E']
	t_rows = ['S'] + pos_keys  
	t_columns = pos_keys + ['E'] 
	#numpy initialize matrix to 0  

	table = numpy.zeros(shape = (len(rows),len(columns)))
	for i in range(len(rows)):
			row_index = t_rows.index(rows[i]) 
			for j in range(len(columns)):
				column_index = t_columns.index(columns[j]) 
				table[i,j] = transition_table[row_index,column_index] 
	
	
	#print_csv('test_trans.csv',table,columns,rows)
	return table




#
#@param sentence 		the sentence list 
#@param pos_list		list of parts of speeches for this particular sentence	
#					obtained from sentence_pos 
#@param	sentence_dic		list of parts of speeches for each word in sentence
#@param	likelihood		likelihood table from training corpus
#@param l_rows		likelihood table rows
#@param	l_columns	likelihood table columns 
def observed_likelihoods(sentence,pos_list,sentence_dic,likelihood_table,l_rows,l_columns ):
	#Rows = POS_list
	#Columns = Words 
	rows = pos_list + ['E']
	columns = sentence + ['E']
	table = numpy.zeros(shape = (len(rows),len(columns))) 
	table[len(rows)-1][len(columns)-1] = 1.0 
	for i in range(len(sentence)): 
		#find part of speech for word 
		word = sentence[i]
		#columns.append(word) #add word to columns list
		#find part of speech for word - list 
		word_pos = sentence_dic[i] 
		#print(word_pos) 

		try:
			l_row_i = l_rows.index(word.lower()) #find likelihood table row 
		except ValueError: 
			l_row_i = -1 #when OOV 
		#print("print likelihood row position\t\t", l_row_i) 
		
		
		#print(sentence[i], word_pos) 
	
		for pos in word_pos: 
			
		#	print(pos) 

			#find column position 
			l_column_i = l_columns.index(pos) 

			#print("l_columns[l_column_i]",l_columns[l_column_i]) 
			#print("l_coumn_i",l_column_i) 
			#find likelihoods from likelihood table 
			if l_row_i != -1:		
				#find likelihood 
				likelihood = likelihood_table[l_row_i][l_column_i] 
			
			else:
				likelihood = 0.00001
			
			
			#print("likelihood",likelihood) 
			#NOTE
			#100K is used for temporary testing
			#Will Evaluate this to be different for all parts of speech 

			#print(columns[i])

			#attach to observed likelihoods table

			row = pos_list.index(pos) 
			column = i

			table[row][column] = likelihood
			#print("table[row][column]",table[row][column]) 

	#print_csv('observed_likelihoods.csv',table,columns,rows)
	return table


def viterbi(observed,sentence,pos_list,transitions ):
	rows = ['S'] + pos_list + ['E']
	columns  = ['S'] + sentence + ['E'] 
	viterbi = numpy.zeros(shape = (len(rows),len(columns))) #lookup 
	path = numpy.zeros(shape = (len(rows),len(columns))) #path 
	#initialize viterbi and path matrix 
	#viterbi will include calculations
	#path will include tuples 
	for i in range(len(rows)):
		for j in range(len(columns)):
			if i == 0 and j== 0:
				viterbi[i][j] = 1 
	
			#if j == len(columns)-1 and i == len(rows)-1:
				#viterbi[i][j] = 1
	
	prev_rows = []
	prev_rows.append(int(0)) 

	for j in range(1,len(columns)):
		prev_list = [] 
		for i in range(1,len(rows)): 
			#print(i,j,"row","column") 
			#print(columns[j]) 
			if j != 0 : 
				like = observed[i-1][j-1]   
				if like > 0: 
					prev_list.append(i) 
					for k in prev_rows:
						previous_vit = viterbi[k][j-1] 
						transition = transitions[k][i-1] 
						calc = previous_vit * like * transition 
						number = viterbi[i][j] 
						if calc > number:
							viterbi[i][j] = calc 
							path[i][j] = k 
		
		prev_rows = prev_list 
#	print_csv('viterbi.csv',viterbi,columns,rows)
#	print_csv('viterbi_path.csv',path,columns,rows)

	
	#Next Step: 
	#Go Through table and find parts of speeches 
	#Output list of tuples (word,pos) 
	

	sentence_tag = [] 
	_row = len(rows)-1 
	for j in range(len(columns)-1,0,-1): 
		value = path[_row][j] 
		value = int(value) 
		tag = (columns[j],rows[_row]) 
		sentence_tag.append(tag) 
		_row = value

	sentence_tag.reverse() 
	#print(sentence_tag) 

	return sentence_tag


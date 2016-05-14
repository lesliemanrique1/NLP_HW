#Leslie Manrique HW 5
import nltk 
import string
from nltk.corpus import stopwords
from math import exp, expm1
import math 


class Query:
	def __init__(self,ID,query):
		self.ID = ID
		self.query = query 

	def print_values(self):
		print(self.ID)
		print(self.query)
	
	def tokenize(self):
		stopset = [word for word in stopwords.words('english')]
		stop_punc = list(string.punctuation)
		stops = stopset+stop_punc

		tokens = nltk.wordpunct_tokenize(self.query) 

		tokens = [w for w in tokens if w.lower() not in stops ] 

		filtered_tokens = [x for x in tokens if not (x.isdigit() or x[0] == '-' and x[1:].isdigit())]



		return filtered_tokens



def tf_idf(sentence,tf_dic,idf_dic):
	vector = [] 	
	for token in sentence:
		tf = 0 
		idf = 0 
		try:
			tf = tf_dic[token]
		except: 
			tf = 0 
		try:
			idf = idf_dic[token]
		except:
			idf = 0 
		vector.append(float(tf*idf))
	return vector 


#list of term frequencies dictionaries per query 
def query_tf_driver(tokenized_queries):
	tf = [] 
	for query in tokenized_queries: 
		tf.append(query_tf(query))
	return tf 

def query_tf(tokenized_string):
	total_terms = len(tokenized_string)
	dic = {} 
	for token in tokenized_string:
		if token not in dic:
			dic[token] = 1 
		else:
			dic[token] = dic[token] + 1 

	for key in dic:
		dic[key] = float(dic[key]) 

	return dic 


def query_tok_occurency(query_tokens):
	number_docs = len(query_tokens)
	dic = {}
	count = 0 
	for query in query_tokens:
		for tok in query:
			if tok not in dic:
				dic[tok] = [0]*number_docs 
				dic[tok][count] = 1 
			else:
				dic[tok][count] = dic[tok][count] +1 
		count = count + 1 

	return dic 

def idf(query_dic,total_docs):
	dic = {}
	for key in query_dic:
		number_docs = 0 
		for count in query_dic[key]:
			if count > 0:
				number_docs = number_docs + 1 

		
		dic[key] = math.log(float(total_docs) / float(number_docs))

	return dic 





def abstract_docs(filename):
	f = open(filename,"r").readlines()
	abstracts = [] 
	string = ""
	cont = False
	for line in f: 
		if ".I" in line: 
			cont = False 
			if len(string)>0:
				abstracts.append(string)
				string = ""
		if ".W" in line:
			cont = True 
		if cont == True:
			string = string + line 
	if len(string)>0:
		abstracts.append(string)

	new_abstracts = []
	for abst in abstracts:
		abst = abst[2:]
		new_abstracts.append(abst)
	return new_abstracts 


def tokenized_queries(query_docs):
	tokenized_que = []
	for query in query_docs:
		tokenized_que.append(query.tokenize()) 
	return tokenized_que

def query_docs(filename):
	f = open(filename,"r").readlines()

	IDS = [] 
	queries = [] 
	WS = [] 
	cont = False 
	string = ""
	for line in f:
		#print(line)
		if ".I" in line:
			cont = False
			if len(string) > 0:
				queries.append(string)
			string = "" 
			part = line.split()
			IDS.append(part[1]) 
		if ".W" in line:
			cont = True 
		if cont == True:
			string = string + line 

	if len(string) > 0 :
		queries.append(string)

	new_queries = []

	for query in queries:
		query = query[2:]
		new_queries.append(query)


	query_docs = [] #query objects 
	length = len(IDS)
	for count in range(length):
		I = IDS[count] 
		qu = new_queries[count]
		query_docs.append(Query(I,qu)) 
	return query_docs 


def tokenize_abstract(abstract_list):
	
	abstract_sentences = [] 
	for abstract in abstract_list:
		sentences = nltk.sent_tokenize(abstract) 
		abstract_sentences.append(sentences)

	
	return abstract_sentences

def abstract_tokens(sentence_tokens):
	abstract_token = [] 
	for doc in sentence_tokens:
		toks = [] 
		for sentence in doc:
			stopset = [word for word in stopwords.words('english')]
			stop_punc = list(string.punctuation)
			stops = stopset+stop_punc

			tokens = nltk.wordpunct_tokenize(sentence) 

			tokens = [w for w in tokens if w.lower() not in stops ] 

			filtered_tokens = [x for x in tokens if not (x.isdigit() or x[0] == '-' and x[1:].isdigit())]

			toks.append(filtered_tokens) 
		abstract_token.append(toks) 



	return abstract_token 


def abstracts_occurence(abstract_tokens):
	total_docs = len(abstract_tokens)
	dic = {} 
	count = 0 
	for doc in abstract_tokens:
		for sentence in doc:
			for tok in sentence: 
				if tok not in dic:
					dic[tok] = [0]*total_docs 
					dic[tok][count] = 1 
				else:
					dic[tok][count] = dic[tok][count] + 1 
		count = count +1 

	return dic 

def abstract_idf(abstract_occurence_dic,total_docs):
	dic = {}

	for key in abstract_occurence_dic:
		number_docs= 0 
		for count in abstract_occurence_dic[key]:
			if count > 0:
				number_docs = number_docs + 1

		#print(number_docs)

		dic[key] = float(total_docs / number_docs )
		dic[key] = math.log(dic[key])

	return dic 

def abstract_tf(abstract_occurence_dic,total_docs):
	abstract_tf_list = [] 
	for count in range(total_docs):
		dic = {} 
		for key in abstract_occurence_dic:
			term = abstract_occurence_dic[key][count]
			if term > 0:
				dic[key] = term 
		abstract_tf_list.append(dic)
	return abstract_tf_list 


def cos_sim(vect1,vect2):
	numerator = 0
	sum_of_squares1 = 0
	sum_of_squares2 =0
	for index in range(len(vect1)):
		numerator = numerator + vect1[index]*vect2[index]
		sum_of_squares1 = sum_of_squares1 + math.pow(vect1[index],2) 
		sum_of_squares2 = sum_of_squares2 + math.pow(vect2[index],2) 
	
	
	sum_of_squares1 = math.sqrt(sum_of_squares1)
	sum_of_squares2 = math.sqrt(sum_of_squares2)
	denominator = float(sum_of_squares1 * sum_of_squares2) 
	divide = 0
	try:
		divide = float(numerator/denominator)
	except: 
		divide = 0 

	return divide


def scoring(queries,abstract_tf_list,abstract_idf,query_tf_list,query_idf):
	
	score_array = [] 
	countQ = 0
	for query in queries: 
		#find query vector 
		v1 = tf_idf(query,query_tf_list[countQ],query_idf)
		#print "v1 \t\t " ,v1 
		countA = 0
		score_tups = []
		for abstract in abstract_tf_list:
			v2 = tf_idf(query,abstract_tf_list[countA],abstract_idf)
			#print "v2 \t\t " ,cv2
			#print v1, v2
			#cosine_sim = cosine_similarity(v1,v2) 
			cosine_sim = cos_sim(v1,v2)
			out = (countQ+1,countA+1,cosine_sim)
			score_tups.append(out)
			#print(cosine_sim)
			#cprint(v2)
			countA = countA+1 
		countQ = countQ + 1 
		score_array.append(score_tups)
	return score_array 


def score_sort(score_array):
	array = [] 
	for query in score_array:
		sorted_by_similarity = sorted(query, key=lambda tup: tup[2],reverse = True )
		array.append(sorted_by_similarity)
	return array 

def out_write(file_name, score_array):
	f = open(file_name, "w")

	for score in score_array:
		for tup in score:
			string = ""
			for t in tup: 
				string = string + str(t) + " "
			f.write(string + "\n")
	f.close()

	print "out file written: " , file_name 




def main():
	
	print("Generating query docs .... ")
	query_docs_list = query_docs("cran/cran.qry") 


	print("tokenizing queries ...")
	tokenized_queries_list = tokenized_queries(query_docs_list) 
	
	print("Generating query dict... ")
	query_dic = query_tok_occurency(tokenized_queries_list)
	

	print("Generating query idf ... ")
	queries_idf = idf(query_dic,len(query_docs_list))


	print("Generating tf list of tf vectors...")
	query_tf_list = query_tf_driver(tokenized_queries_list)


	print("Generating abstract docs ... ")

	abstract_doc_list = abstract_docs("cran/cran.all.1400")
	#print(abstract_doc_list)
	#print(len(abstract_doc_list))

	print("Tokenizing abstracts ... ")
	abst_sentence_tokens = tokenize_abstract(abstract_doc_list)

	abst_tokens = abstract_tokens(abst_sentence_tokens)
	

	print("Computing abstract corpus idf ... ")
	abstract_tok_occurence = abstracts_occurence(abst_tokens)

	
	abst_idf = abstract_idf(abstract_tok_occurence,len(abstract_doc_list))


	print("computing tfs for each document ... ")
	
	abst_docs_tf_list = abstract_tf(abstract_tok_occurence,len(abstract_doc_list))

	print("Generating Scoring ..." )


	score_list = scoring(tokenized_queries_list,abst_docs_tf_list,abst_idf,query_tf_list,queries_idf)

	score_list = score_sort(score_list) 

	print("Generating file ...")
	out_write("out.txt", score_list)




main()  










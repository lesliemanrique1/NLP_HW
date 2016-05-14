import viterbi
import timeit 
import sys 

def viterbi_run(training, test_file): 

	#returns a list of sentence list containing tuples (word,part of speech) 
	

	corpus_list = viterbi.corpus_list(training) 

	#creates a dictionary of corpus part of speech tag : occurences 
	corpus_dictionary = viterbi.corpus_dictionary(training) 

	#pos_keys 
	keys = viterbi.key_list(corpus_dictionary) 

	#creates the prior_probabilities transitions table for the entire corpus 


	prior_probabilities_table = viterbi.transition_table(corpus_dictionary,corpus_list)


	#creates a word dictionary 
	#word: list of part of speeches and increment occurences of word as part of speech 
	word_dic = viterbi.word_dic(corpus_list,keys) 


	#word_keys
	words = viterbi.key_list(word_dic)


	#likelihood_table 
	likelihood_table  = viterbi.word_freq(corpus_dictionary,word_dic)


	#Emissions and Transitions 
	sentences = viterbi.corpus_list_2(test_file) 

	error_list = [] 
	error_list_i = [] 
	new_sentences = [] 
	count = 0 
	for sentence in sentences:
		trans = viterbi.sentence_tag(sentence,keys,words,likelihood_table)
		s_pos = viterbi.sentence_pos(trans)
		transition_table = viterbi.transition_probabilities(trans,s_pos,prior_probabilities_table,keys)

		observed_like = viterbi.observed_likelihoods(sentence,s_pos,trans,likelihood_table,words,keys)
		vit_sent = viterbi.viterbi(observed_like,sentence,s_pos,transition_table) 
<<<<<<< HEAD
		new_sentences.append(vit_sent) 
=======
>>>>>>> 64c28348f9bebad1b1737107c5bbb54b4b027e1d
	"""
		errors = 0 
		for p in vit_sent:
			if p[1] == 'S':
				errors=errors+1 
	
		new_sentences.append(vit_sent) 
		if(errors>0):
			error_list.append(vit_sent) 
			error_list_i.append(count)
		count=count+1

	print(error_list)
	print(error_list_i)
	"""
	return new_sentences #returns list of sentence 

#output into file named Leslie_Manrique_WSJ_23.pos  
def output_file(tag_list, write_file):
	f = open(write_file,'w') 
	with f as out:
		for sentence in tag_list:	
			for pair in sentence:
				row = pair[0] + "\t" + pair[1] + "\n"
				out.write(row) 
			out.write("\n") 
	f.close()


def file_merge(file1,file2):
	filenames = [file1,file2]
	with open('merged.txt', 'w') as outfile:
		for fname in filenames:
			with open(fname) as infile:
				for line in infile:
					outfile.write(line)
	
	return "merged.txt"
	

def main():
	
	if len(sys.argv) != 4:
		print("Error: program takes in three arguments - file1.txt , file2.txt,file3.txt") 
		exit() 
	
	
	training = sys.argv[1]
	development = sys.argv[2] 
	run_file = sys.argv[3] 

	merged = file_merge(training,development) 

	out= "Leslie_Manrique_WSJ_23.pos"

	print("...running algorithm") 
	start = timeit.default_timer()
	tag_list = viterbi_run(merged,run_file) 
	stop = timeit.default_timer()
	print("viterbi algorithm elapsed time : %d",stop-start) 
	for sentence in tag_list:
		del sentence[-1] 
	print("...creating csv") 
	output_file(tag_list, out) 
	print("...done") 	


main() 



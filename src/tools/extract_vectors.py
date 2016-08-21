#!/usr/bin/python

import sys

help_s = '''
This script is used to extract the vector representations for a given list of words from a collection of vector representations. 
Given (i) a file specifying the words for which we want the vector representations to be extracted
and (ii) a file into which are specified the vector representations for a collection of words, 
the script builds a new file containing the vector representations of the specified words (that have be found in the collection).

Inputs: 

	(i) the list of words for which we want to extract the vector representations
		format: one word per line
		e.g.
			fish
			reduced
			...
	
	(ii) collection of vector representations
		One representation per line / only extracting the word matters
		format: word[space]vector_representation
		e.g.
			reduced -0.050236 -0.013199 -0.041371...
			alcohol -0.017343 -0.095251 0.015348...
			fish -0.058083 0.052891 0.001379 0.024985...
			...
			
		Note: all '_' symbol in the file will be modified by a space, e.g. machine_learning will transformed to 'machine learning'
		
Parameters: 
	[1] file containing the words for which we want to extract the vector representations
	[2] file containing all the vector representations
	[3] output file which will contain the vector representations for the specified words
	[6] result file directory to store the global evaluation result
		
version: 0.1
'''



if(len(sys.argv) != 6):
	print help_s
	print sys.argv
	exit()

vocabulary_file_path = sys.argv[1]
vector_file_path = sys.argv[2]
vector_file_extraction_path = sys.argv[3]
global_evaluation_result_file = sys.argv[4]

print "vocabulary file: ",vocabulary_file_path
print "vector file: ",vector_file_path
print "vector file extraction: ",vector_file_extraction_path

print "Loading vocabulary"

vocabulary = set()

with open(vocabulary_file_path) as data_file:	
	for l in data_file:
		vocabulary.add(l.strip())

size_voc = len(vocabulary)
print "vocabulary loaded: ",len(vocabulary)

with open(vector_file_extraction_path,"w") as vector_file_extraction:
	
	with open(vector_file_path) as vector_file:	
		for l in vector_file:
			data_line = l.split()
			label = data_line[0].replace("_", " ") # for wordvec representation 
			if(label in vocabulary):
				vector_file_extraction.write(l)
				vocabulary.remove(label)
				print "Adding ",label, " ",str(size_voc - len(vocabulary)),"/",str(size_voc)




# Added by Jie
intersection_pairs = sys.argv[5]
intersection_pairs_number = sum(1 for line in open(intersection_pairs))
with open(global_evaluation_result_file,'a') as fa:
	fa.write(',%d,%d' % (intersection_pairs_number, size_voc - len(vocabulary)))
				
print "Extraction: ",str(size_voc - len(vocabulary)),"/",str(size_voc)
print "Consult: ",vector_file_extraction_path
print "ended extract_vectors.py"
print "---------------             --------------------          ------------------ \n"


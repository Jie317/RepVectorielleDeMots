#!/usr/bin/python

import sys


help_s = '''

Script used to generate a benchmark considering specified parameters.

As input data we have:

(i) A file defining a set of descriptors for a set of words (mapping term/descriptors file).
To each word is associated a set of descriptors, each of them being of a specific level in [1,4]
As an example we have the following data associated to the word 'orange': 
	
	word              : orange	
	descriptor level 1: fruits	
	descriptor level 2: citrus fruits	
	descriptor level 3: citrus fruits	
	descriptor level 4: orange
	
	(we can have two similar descriptors for a same word in different levels)
	
	The format of the file is: 
	word[TAB]DESCRIPTOR_LEVEL_1[TAB]DESCRIPTOR_LEVEL_2[TAB]DESCRIPTOR_LEVEL_3[TAB]DESCRIPTOR_LEVEL_4
	e.g.
	  animal	animal	domestic animal	domestic animal	leather
	  black currant	fruits	black fruits	fresh black fruits	black currant
	  black currant candy	fruits	black fruits		
	  caramel 	empyreumatic	cocoa/caramel	cocoa/caramel	caramel
	  cheese	fermented	fermented	fermented	

Considering that we have a collection of word vector representation, 
the aim of the script is, considering a given descriptor level (in [1,4]), 
to extract the pairs of (word,descriptor) for which we have the vector 
representations of both the word and the descriptor.
	
Parameters:
	[1] data file containing the mapping term descriptors
	[2] level of descriptors to consider
	[3] vocabulary of words for which we have the vectors (one word per line)
	[4] output vocabulary containing all the descriptors and the terms used: 
		this file contains all the words that are in a selected pair
	[5] output file containing all the valid pairs
	[6] result file directory to store the global evaluation result

version 0.1
'''


#test
def cosine_similarity(v1,v2):
    "compute cosine similarity of v1 to v2: (v1 dot v2)/{||v1||*||v2||)"
    sumxx, sumxy, sumyy = 0, 0, 0
    for i in range(len(v1)):
        x = v1[i]; y = v2[i]
        sumxx += x*x
        sumyy += y*y
        sumxy += x*y
    den = math.sqrt(sumxx*sumyy)
    if(den == 0): return 0
    return sumxy/den






	
if(len(sys.argv) != 7):
	print help_s
	exit()

data_file_path = sys.argv[1]
level = int(sys.argv[2])
vector_vocabulary_path = sys.argv[3]
output_vocabulary_path = sys.argv[4] # where the vocabulary containing the words and associated descriptors will be stored
output_valid_pairs_path = sys.argv[5]
global_evaluation_result_file = sys.argv[6]

print "data file: ",data_file_path
print "level: ",level

if(level < 1 or level > 4):
	print "Level value has to be set into [1,4]"
	exit()

entries = {}
entries_not_direct_match = {}
voc_descriptors = set()

with open(data_file_path) as data_file:
	
	for l in data_file:
		data_line = l.strip().split("\t")
		
		for i in range(0,len(data_line)):
			data_line[i] = data_line[i].strip().lower()
	
		label = data_line[0]
		
		
		if len(data_line) == 5 and (label not in entries) :
			specific_descriptor = data_line[level]
			entries[label] = data_line
			if not label == specific_descriptor:
				entries_not_direct_match[label] = data_line
		else:
			print "**",data_line

print "------------------------------------------------------------"

with open(output_vocabulary_path,"w") as output_voc:
	voc_complete = set()
	for e in entries:
		voc_complete.add(e)
		for v in entries[e]:
			voc_complete.add(v)
			voc_descriptors.add(v)
	
	for v in voc_complete:
		output_voc.write(v+"\n")	
		
for e in entries_not_direct_match:
	word_a = e
	word_b = entries_not_direct_match[e][level]
	print "'"+word_a+"'"," : "+"'"+word_b+"'"
	

print "------------------------------------------------------------"

print "Length ",len(entries)
print "Length No direct match ",len(entries_not_direct_match)
print "voc descriptor length: ",len(voc_descriptors)

print "Loading vocabulary from: ",vector_vocabulary_path
vocabulary = set()
with open(vector_vocabulary_path) as voc_file:
	for l in voc_file: 
		vocabulary.add(l.strip().replace("_"," "))
		
print "Vocabulary size: ",len(vocabulary)

valid = 0
with open(output_valid_pairs_path,"w") as output_valid_pairs:
	
	for e in entries_not_direct_match:

		word_a_exists = False
		word_b_exists = False
		
		word_a = e
		word_b = entries_not_direct_match[e][level]
		
		if(word_a in vocabulary): word_a_exists = True
		if(word_b in vocabulary): word_b_exists = True
		
		if(word_a_exists and word_b_exists and word_a != word_b):
			output_valid_pairs.write(word_a+"\t"+word_b+"\n") 
			valid +=1
		else:
			print "*** '"+word_a+"'", str(word_a_exists)," : "+"'"+word_b+"'",str(word_b_exists) 


# Added by Jie
if global_evaluation_result_file != "0":
	with open(global_evaluation_result_file,'a') as fa:
		fa.write(',%d,%d,%d' % (len(vocabulary), len(entries_not_direct_match), valid))

		
print "Length No direct match ",len(entries_not_direct_match)
print "Valid No direct match ",str(valid),"/",len(entries_not_direct_match)
print "Valid pairs stored at: ",output_valid_pairs_path
print "ended generate_benchmark.py"
print "---------------             --------------------          ------------------ \n"




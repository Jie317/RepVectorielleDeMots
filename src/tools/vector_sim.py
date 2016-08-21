#!/usr/bin/python

help_s = '''
Script used to compute word cosine similarity based on word vector representations.
It can be used to compute 
	(i) the similarity between two word vector representations.
	(ii) the similarity between a given words and all other words for which we have vector representations
	
Parameters: 
	[1] vector format (values 0 if uncompressed, 1 if compressed)
	[2] separator between the word and its vector (values: tab or space)
	[3] separator between the vector values (values: tab or space)
	[4] vector file: the file containing the vector representations
	[5] word_a
	[6] word_b (optional)
	
If no word_b specified the script will compute the similarity with all the other vectors
The script doesn't support the composed words (e.g. machine learning)

version: 0.2
 
'''

import sys
import linecache
#from sklearn.metrics.pairwise import cosine_similarity
import math

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

def loadVectorRepresentation(filename, lineNumber, vec_format, size):
	data  = linecache.getline(filename, lineNumber).split() # the original variable in split is vec_format_sep
	return loadVectorRepresentationInner(data, vec_format, size)
	
def loadVectorRepresentationInner(data, vec_format, size):
	
	data.pop(0)
	if(vec_format == UNCOMPRESSED_VECTOR):
		vec_word = [float(x) for x in data]

	elif(vec_format == COMPRESSED_VECTOR):
		vec_word = []
		for i in range(0,size): vec_word.append(0)
		
		for s in data: 
			data2 = s.split(":")
			vec_word[int(data2[0])] = float(data2[1])
	else:
		print "Error, unrecognized vector format: ",vec_format
		exit()
	return vec_word

if(len(sys.argv) < 6 or len(sys.argv) > 7):
	print help_s
	exit()

UNCOMPRESSED_VECTOR = 0
COMPRESSED_VECTOR   = 1

vec_format = int(sys.argv[1])
vec_format_sep_string1 = sys.argv[2]
vec_format_sep_string2 = sys.argv[3]
vector_file = sys.argv[4]
word = sys.argv[5]
word_b = None

if(len(sys.argv) == 7):
	word_b = sys.argv[6]

vec_format_sep = None
if((vec_format_sep_string1 == "tab" or vec_format_sep_string1 == "space")
   and (vec_format_sep_string2 == "tab" or vec_format_sep_string2 == "space")):
	print 'The separators are accepted'
else:
	print "Invalid vector separator format: ",vec_format_sep_string1,+' '+vec_format_sep_string1

print "Loading vectors from ",vector_file


print "Loading index"
voc_index = {}
vec_size = None

if(vec_format == UNCOMPRESSED_VECTOR):
	line_c = 1
	with open(vector_file) as v_file:
		for l in v_file:
			data = l.strip().split()
			voc_index[data[0].lower()] = line_c
			v_size = len(data)-1
			if(vec_size != None and vec_size != v_size):
				print "Vector representation is corrupted for ",data[0]
			else:
				vec_size = v_size
				
			line_c+=1
			
elif(vec_format == COMPRESSED_VECTOR):
	line_c = 1
	with open(vector_file) as v_file:
		loadSize = True
		for l in v_file:
			if(loadSize): 
				vec_size = int(l.strip())
				loadSize = False
			else:
				data = l.strip().split()
				voc_index[data[0].lower()] = line_c	
			line_c+=1
else:
	print "Invalid vector format:",vec_format
	exit()
	
	
print "Vocabulary size", str(len(voc_index)), " vector size:",str(vec_size)
wordInVoc = word in voc_index
print word, " in vocabulary ", wordInVoc

if(not wordInVoc):
	print "Stop process"
	exit()


# retrieve corresponding line and remove first element (label)
vec_word  = loadVectorRepresentation(vector_file, voc_index[word], vec_format, vec_size)


if(word_b != None):
	word_bInVoc = word_b in voc_index
	print word_b, " in vocabulary ", word_bInVoc
	if(not word_bInVoc):
		print "Stop process"
		exit()
	
	vec_word_b  = loadVectorRepresentation(vector_file, voc_index[word_b], vec_format, vec_size)
	print "sim",str(cosine_similarity(vec_word, vec_word_b))

else: # compute all similarities
	
	similarities = {}
	best_sim = 0
	best_sim_label = None
	line_c = 1
	
	word_plural = None
	if(word[-1] != "s"): word_plural = word+"s"
		
	with open(vector_file) as v_file:
		
		header = vec_format == COMPRESSED_VECTOR
		
		for l in v_file:
			
			if(header): 
				header = False
				continue
				
			
			vec_word_b = l.strip().split()
			label_word_b = vec_word_b[0]
			vec_word_b = loadVectorRepresentationInner(vec_word_b, vec_format, vec_size)
			sim = cosine_similarity(vec_word, vec_word_b)
			
			similarities[label_word_b] = sim
			
			if(label_word_b != word and label_word_b != word_plural and sim > best_sim):
				best_sim = sim
				best_sim_label = label_word_b
			
			if(line_c % 10000 == 0): print str(line_c),"/",str(len(voc_index)), "\tbest so far: ",best_sim_label,"\tsim=",str(best_sim)
			line_c += 1
		
		limit = 100
		for w in sorted(similarities, key=similarities.get, reverse=True):
			
			print w, "\t", str(similarities[w])
			limit -= 1
			#if(limit == 0): break
	
	
	



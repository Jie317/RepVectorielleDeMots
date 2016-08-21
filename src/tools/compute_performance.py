#!/usr/bin/python

help_s = '''
Script used to compute the performance of an approach (vector representations) according to a set of pairs of words.
It is expected that considering a vocabulary V={w_1,w_2,...} the cosine similarity between two vector representations 
of two words w_i and w_j composing a given pair (w_i,w_j) should give the highest similarity score among all the pairs in w_i x V.

Parameters:
	[1] vector format (values 0 if uncompressed, 1 if compressed)
	[2] vector file: the file containing the vector representations
	[3] pair file: one pair per line
	[4] output file
	[5] result file path to store the global evaluation result
	[6] current model name

'''

import sys
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

def loadVectorRepresentation(filename, lineNumber, vec_format, vec_format_sep, size):
	data  = linecache.getline(filename, lineNumber).split(vec_format_sep)
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
	
def compute_lambda_difficulty(voc, vectors):
	values = []
	values_global = []
	for word1 in voc:
		word1_vec = vectors[word1]
		for word2 in voc:
			if word2 != word1: 
				word2_vec = vectors[word2]
				values.append(cosine_similarity(word1_vec, word2_vec))
		values_global.append(max(values))
		values = []
	return sum(values_global)/float(len(voc))
			


if(len(sys.argv) != 7):
	print help_s
	exit()



UNCOMPRESSED_VECTOR = 0
COMPRESSED_VECTOR   = 1



vec_format = int(sys.argv[1])
vector_file = sys.argv[2]
pairs_file = sys.argv[3]
result_file_path = sys.argv[4]
global_evaluation_result_path = sys.argv[5]
approach = sys.argv[6]


print "Loading vectors from ",vector_file


print "Loading index"
vectors = {}
vec_size = None

if(vec_format == UNCOMPRESSED_VECTOR):
	
	with open(vector_file) as v_file:
		for l in v_file:
			data = l.split()
			# we replace _ per ' ' for word2vec representations
			label = data[0].lower().replace("_"," ")
			data.pop(0)
			vectors[label] = map(float, data)
			v_size = len(data)
			if(vec_size != None and vec_size != v_size):
				print "Vector representation is corrupted for ",data[0]
			else:
				vec_size = v_size
			
elif(vec_format == COMPRESSED_VECTOR):
	
	with open(vector_file) as v_file:
		loadSize = True
		for l in v_file:
			if(loadSize): 
				vec_size = int(l.strip())
				loadSize = False
			else:
				data = l.strip().split()
				label = data[0].lower().replace("_"," ")
				data.pop(0)
				vec_tmp = [0] * vec_size
				for d in data:
					info = d.split(":")
					vec_tmp[info[0]] = info[1]
				vectors[label] = map(float, vec_tmp)
else:
	print "Invalid vector format:",vec_format
	exit()
	


print "loading pairs"

global_error = 0
process_pairs = 0
total_pairs   = 0
prediction = 0
descriptor_voc = set()
pair_ranks_fn = pairs_file.replace('intersection.pair',approach+'_term_concepts.ranks')
pair_sims_fn = pairs_file.replace('intersection.pair',approach+'_term_concepts.sims')

with open(result_file_path,"w+") as result_file,  open(pairs_file) as pfile, open(pair_ranks_fn,'w+') as pair_ranks, open(pair_sims_fn, 'w+') as pair_sims:
		for l_voc in pfile: 
			descriptor_voc.add(l_voc.split()[1])
		
		pfile.seek(0)
		for l in pfile: 
			similarities = {}
			pair = l.strip().split("\t")
			
			word_a =  pair[0]
			word_b =  pair[1]
			print "-------------------------------"
			print "Processing ",word_a,"/",word_b
			print "-------------------------------"		
			
			total_pairs +=1
			
			if(not word_a in vectors):
				print "** Cannot find ",word_a
				continue
			if(not word_b in vectors):
				print "** Cannot find ",word_b
				continue
				
				
			process_pairs+=1
			print process_pairs
			
			vec_word_a = vectors[word_a]
		
			#print vec_word_a
	
			# Compute ranking

			for word in descriptor_voc:
				vec_word = vectors[word]
				sim = cosine_similarity(vec_word_a, vec_word)
				similarities[word] = sim
			
			
			rank = 1
			rank_word_b = None
			
			for word in sorted(similarities, key=similarities.get, reverse=True):
				
				pair_sims.write('%s %s\t%.5f\n' % (word_a, word, similarities[word]))
				pair_ranks.write('%s %s\t%d\n' % (word_a, word, rank))
				
				print rank,"\t",word
				if(word == word_b): 
					rank_word_b = rank
					if rank == 1: prediction += 1
				rank+=1
			
			print 'Prediction ratio: %.3f' % (float(prediction)/total_pairs)
			print "rank", str(rank),"/",str(len(similarities))
			result_file.write(pair[0]+"\t"+pair[1]+"\t"+str(rank_word_b)+"\t"+str(len(similarities))+"\n")
			global_error += rank_word_b
			

print global_error,process_pairs
# Added by Jie
lambda_difficulty = compute_lambda_difficulty(descriptor_voc, vectors)

with open(global_evaluation_result_path,'a') as fa:
	if process_pairs == 0 or len(descriptor_voc) == 0:
		process_pairs = 0.1
		descriptor_voc.add('pass')
	fa.write(',%d,%.2f,%d,%.3f,%.3f,%.3f\n' % (global_error, float(global_error)/process_pairs, len(descriptor_voc), float(global_error)/process_pairs/len(descriptor_voc), lambda_difficulty, float(prediction)/total_pairs))

print "Consult results at: ",result_file_path
print "processed pairs:",str(process_pairs),"/",total_pairs
print "Error rate global: ",str(global_error),"\t","averaged: ",str(global_error/process_pairs)
print "ended compute_performance.py"
print "---------------             --------------------          ------------------ \n"
			
	


